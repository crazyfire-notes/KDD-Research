# This code is for converting packets to DRAPA format data structures

import os
import pyshark
import datetime
import nest_asyncio
from concurrent.futures import ProcessPoolExecutor
from filelock import FileLock, Timeout


def get_service_name(protocol, port):
    service_mapping = {
        "tcp": {
            "21": "ftp",
            "22": "ssh",
            "23": "telnet",
            "25": "smtp",
            "53": "dns",
            "79": "finger",
            "80": "http",
            "110": "pop3",
            "111": "rpcbind",
            "113": "auth",
            "123": "ntp/u",
            "143": "imap",
            "443": "https",
            "8080": "http-proxy",
            # for OT service
            "102": "s7comm",
            "502": "modbus",
            "789": "dnp3",
            "1080": "socks",
            "1911": "trihedral-vts",
            "2222": "iec-104",
            "2404": "iec-61850",
            "2455": "bacnet",
            "5006": "melsec-fx",
            "5007": "melsec-q",
            "5094": "hart-ip",
            "9600": "omron-fins",
            "20547": "proconos",
            "34962": "rslinx",
            "44818": "ethernet-ip",
        },
        "udp": {
            "53": "dns",
            "67": "dhcp",
            "68": "dhcp",
            "123": "ntp",
            # for OT service
            "161": "snmp",
            "162": "snmptrap",
            "2223": "iec-104",
            "2404": "iec-61850",
            "5094": "hart-ip",
            "9600": "omron-fins",
            "18245": "enip-udp",
            "18246": "dnp3",
            "47808": "bacnet",
        }
    }

    return service_mapping.get(protocol.lower(), {}).get(port, protocol.lower())


def get_pcap_paths(pcap_root):
    pcap_paths = []
    for root, _, files in os.walk(pcap_root):
        pcap_paths.extend(
            os.path.join(root, file)
            for file in files
            if file.endswith('.cap')
        )
    return pcap_paths


def get_pcap_packets(pcap_path):
    capture = pyshark.FileCapture(pcap_path)
    capture_packets = list(capture)
    capture.close()
    return capture_packets


def get_basic_packet_info(packet):
    try:
        start_date = datetime.datetime.fromtimestamp(
            float(packet.frame_info.time_epoch)
        ).strftime("%m/%d/%Y")
        start_time = datetime.datetime.fromtimestamp(
            float(packet.frame_info.time_epoch)
        ).strftime("%H:%M:%S")
        # pcap 中無法直接取得，會於後續依照相同的 service, src_port, dest_port, src_ip, dest_ip 來計算
        duration = "00:00:00"
        protocol = packet.transport_layer.lower()
        src_port = packet[packet.transport_layer].srcport
        dest_port = packet[packet.transport_layer].dstport
        src_ip = packet.ip.src
        dest_ip = packet.ip.dst
        service = get_service_name(protocol, dest_port)

        return start_date, start_time, duration, protocol, service, src_port, dest_port, src_ip, dest_ip
    except AttributeError:
        
        return None, None, None, None, None, None, None, None


def get_packet_duration(packet_infos):
    # the packet with the same service, src_port, dest_port, src_ip, dest_ip will be in the same session
    connections = {}
    for packet_info in packet_infos:
        if packet_info[0] is None:
            continue
        timestamp = datetime.datetime.strptime(
            f"{packet_info[0]} {packet_info[1]}",
            "%m/%d/%Y %H:%M:%S"
        )
        service = packet_info[4]
        src_port = packet_info[5]
        dest_port = packet_info[6]
        src_ip = packet_info[7]
        dest_ip = packet_info[8]
        
        if (service, src_port, dest_port, src_ip, dest_ip) not in connections:
            connections[(service, src_port, dest_port, src_ip, dest_ip)] = [timestamp]
        else:
            connections[(service, src_port, dest_port, src_ip, dest_ip)].append(timestamp)
            
    for key, timestamp in connections.items():
        connections[key] = max(timestamp) - min(timestamp) if len(timestamp) > 1 else datetime.timedelta(0)
        
    return connections


def transfer_to_DRAPA_format(packet_infos):
    packet_durations = get_packet_duration(packet_infos)
    packet_DRAPA_format = []
    for packet_info in packet_infos:
        if packet_info[0] is None:
            continue
        start_date = packet_info[0]
        start_time = packet_info[1]
        protocol = packet_info[3]
        service = packet_info[4]
        src_port = packet_info[5]
        dest_port = packet_info[6]
        src_ip = packet_info[7]
        dest_ip = packet_info[8]
        duration = packet_durations.get(
            (packet_info[4], packet_info[5], packet_info[6], packet_info[7], packet_info[8]),
            datetime.timedelta(0)
        )
        
        packet_DRAPA_format.append(
            f"{start_date},{start_time},{duration},{protocol},{service},{src_port},{dest_port},{src_ip},{dest_ip}"
        )
        
    return packet_DRAPA_format


def process_pcap_file(pcap_path):
    output_csv = f"../../Datasets/{os.path.basename(pcap_path).split('.')[0]}.csv"
    lock_file = f"{output_csv}.lock"
    
    try:
        with FileLock(lock_file, timeout=0):
            if os.path.exists(output_csv):
                print(f"{os.path.basename(output_csv)} already exists. Skipping.")
                return pcap_path

            print('Processing', os.path.basename(pcap_path).split('.')[0], '...')
            pcap_packets = get_pcap_packets(pcap_path)
            packet_infos = [get_basic_packet_info(packet) for packet in pcap_packets if packet.transport_layer and packet.ip]
            packet_DRAPA_format = transfer_to_DRAPA_format(packet_infos)

            with open(output_csv, 'w') as f:
                f.write('Start Date,Start Time, Duration, Protocol, Service, Src Port, Dest Port, Src IP, Dest IP\n')
                f.write('\n'.join(packet_DRAPA_format))
                f.write('\n')
            print(f"{os.path.basename(pcap_path).split('.')[0]}.csv has been saved")
    except Timeout:
        print(f"{os.path.basename(pcap_path)} is being processed by another process. Skipping.")
        return pcap_path

    return pcap_path


def main():
    pcap_root = '../../Datasets/'
    # get all pcap paths
    pcap_paths = get_pcap_paths(pcap_root)
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Use list() to iterate through generator and get results.
        results = list(executor.map(process_pcap_file, pcap_paths))

        for result in results:
            print(f"Processed {result}")


if __name__ == '__main__':
    nest_asyncio.apply()
    main()
