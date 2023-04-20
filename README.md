# KDD-Research

This repo is for KDD Dataset Research and Any kinds of Related works.

## About KDD Dataset / 關於 KDD 資料集

- KDD 資料集是一個著名的網路流量數據資料集，其中最有名的資料及有兩個，一、KDD-99 資料集，二、NSL-KDD 資料集。本記錄會以 NSL-KDD 為主作紀錄。
- 關於 KDD 資料集中，General 的資訊如下，
  - 資料集中有四種不同的攻擊，分別是 DoS (服務阻斷), Probe (探測), R2L (遠端操作), U2R (使用者權限提升)。
    - 其中四種類別還分別有以下子類別：
      | Classes | DoS | Probe | R2L | U2R |
      | --- | --- | --- | --- | --- |
      | Subclasses | apache2, back, land, neptune, mailbomb, pod, processtable, smurf, teardrop, udpstorm, worm | ipsweep, mscan, nmap, portsweep, saint, satan | ftp_write, guess_passwd, httptunnel, imap, multihop, named, phf, sendmail, snmpgetattack, spy, snmpguess, warezclient, warezmaster, xlock, xsnoop | buffer_overflow, loadmodule, perl, ps, rootkit, sqlattack, xterm |
      | Total | 11 | 6 | 15 | 7 |
  - 而其中每一條流量數據都有包含 43 個特徵，包含 41 個數據原始特徵，和一個標籤 (正常 / 攻擊)，和一個分數 (流量嚴重性)，各欄位分別是
    - TCP 基礎連線特徵
      1. duration: 連線持續時間，以秒為單位，範圍為 0 ~ 58329。
        > 其定義方式:
        >
        > - TCP: TCP 的第一次握手 (SYN) 到第三次握手 (FIN/ACK) 或者失敗握手 (RST) 的時間。
        > - UDP: UDP 則是每一個 UDP 當作一個連線，所以時間就是每一個 UDP 的時間。
        >   > - duration = 0 在 dataset 中大量出現的原因是因為這個連接持續時間不到 1 sec。
      1. protocol_type: 連線協定，有三種，`tcp`, `udp`, `icmp`
      2. service: 目標主機的服務類型 (所連線的服務)，共 70 種，`aol`, `auth`, `bgp`, `courier`, `csnet_ns`, `ctf`, `daytime`, `discard`, `domain`, `domain_u`, `echo`, `eco_i`, `ecr_i`, `efs`, `exec`, `finger`, `ftp`, `ftp_data`, `gopher`, `harvest`, `hostnames`, `http`, `http_2784`, `http_443`, `http_8001`, `imap4`, `IRC`, `iso_tsap`, `klogin`, `kshell`, `ldap`, `link`, `login`, `mtp`, `name`, `netbios_dgm`, `netbios_ns`, `netbios_ssn`, `netstat`, `nnsp`, `nntp`, `ntp_u`, `other`, `pm_dump`, `pop_2`, `pop_3`, `printer`, `private`, `red_i`, `remote_job`, `rje`, `shell`, `smtp`, `sql_net`, `ssh`, `sunrpc`, `supdup`, `systat`, `telnet`, `tftp_u`, `tim_i`, `time`, `urh_i`, `urp_i`, `uucp`, `uucp_path`, `vmnet`, `whois`, `X11`, `Z39_50`
      3. flag: 連線是否正常或錯誤 (連線狀態)，共有 11 種，`OTH`, `REJ`, `RSTO`, `RSTOS0`, `RSTR`, `S0`, `S1`, `S2`, `S3`, `SF`, `SH`
        > 其表示了連線是否有依照協定要求開始或者完成。
        >
        > - `SF`: 表示連線正常建立且正常終止
        > - `S0`: 表示只接收到 SYN 封包，但是沒有回應 SYN/ACK 封包
      4. src_bytes: 來源端傳送到目的端的 bytes 數量，以 bytes 為單位，範圍為 0 ~ 1,379,963,888
      5. dst_bytes: 目的端傳送到來源端的 bytes 數量，以 bytes 為單位，範圍為 0 ~ 1,309,937,401
      6. land: 來源端和目的端是否為同一個 IP, 有 `0` (不是) 和 `1` (是)
      7. wrong_fragment: 連線中有多少錯誤的封包，範圍為 0 ~ 3
      8. urgent: 連線中有多少 urgent 的封包，範圍為 0 ~ 14
    - TCP 連線內容特徵
      10. hot: 連線中訪問系統敏感資源的次數，範圍為 0 ~ 101
      11. num_failed_logins: 連線中有多少次登入失敗，範圍為 0 ~ 5
      12. logged_in: 連線中是否有成功登入，有 `0` (沒有) 和 `1` (有)
      13. num_compromised: 連線中有多少次被入侵, 數值
    1.  root_shell: 連線中有 root shell, 數值
    2.  su_attempted: 連線中有多少次嘗試使用 su, 數值
    3.  num_root: 連線中有多少次使用 root, 數值
    4.  num_file_creations: 連線中有多少次建立檔案, 數值
    5.  num_shells: 連線中有多少次使用 shell, 數值
    6.  num_access_files: 連線中有多少次存取檔案, 數值
    7.  num_outbound_cmds: 連線中有多少次傳送指令, 數值
    8.  is_host_login: 連線中是否有 host 登入, 有 `0` (沒有) 和 `1` (有)
    9.  is_guest_login: 連線中是否有 guest 登入, 有 `0` (沒有) 和 `1` (有)
    10. count: 連線中有多少次封包, 數值
    11. srv_count: 連線中有多少次 server 封包, 數值
    12. serror_rate: 連線中有多少次封包有 error, 數值
    13. srv_serror_rate: 連線中有多少次 server 封包有 error, 數值
    14. rerror_rate: 連線中有多少次封包有 error, 數值
    15. srv_rerror_rate: 連線中有多少次 server 封包有 error, 數值
    16. same_srv_rate: 連線中有多少次封包是同一個 server, 數值
    17. diff_srv_rate: 連線中有多少次封包是不同的 server, 數值
    18. srv_diff_host_rate: 連線中有多少次 server 封包是不同的 host, 數值
    19. dst_host_count: 連線中有多少次封包是目的端的 host, 數值
    20. dst_host_srv_count: 連線中有多少次封包是目的端的 server, 數值
    21. dst_host_same_srv_rate: 連線中有多少次封包是目的端的 server, 數值
    22. dst_host_diff_srv_rate: 連線中有多少次封包是目的端的不同 server, 數值
    23. dst_host_same_src_port_rate: 連線中有多少次封包是目的端的相同來源端 port, 數值
    24. dst_host_srv_diff_host_rate: 連線中有多少次封包是目的端的不同 server 的 host, 數值
    25. dst_host_serror_rate: 連線中有多少次封包是目的端的 error, 數值
    26. dst_host_srv_serror_rate: 連線中有多少次封包是目的端的 server 的 error, 數值
    27. dst_host_rerror_rate: 連線中有多少次封包是目的端的 error, 數值
    28. dst_host_srv_rerror_rate: 連線中有多少次封包是目的端的 server 的 error, 數值
    29. class: 連線的類別, 有 `normal` (正常) 和 `anomaly` (異常)
    30. difficulty_level: 連線的難度, 數值，難度從 1~21，越高越難
- NSL-KDD 為 KDD-99 的修訂版本，主要旨在解決 KDD-99 資料集中的一些問題，包含：
  - KDD-99 中有不必要冗余的資料，可以避免 Classifiers 不會因為冗余的資料而有偏向性。 (這部分可以再做討論，究竟冗余資料是哪一種，而且會怎麼影響 Classifiers)
  - Testing set 中沒有重複的紀錄，因此 learning 的表現不會因為受到頻繁紀錄檢測率更高的方法而有所影響
  - 對於不同難度資料的分類，KDD-99 中的攻擊類別是不平衡的，而 NSL-KDD 中的攻擊類別是平衡的
  - 訓練集和測試集中的數量紀錄是合理的，因此使用整個資料集做訓練是可行且合理的，無需再做切割，所有的實驗都將可以有一致性和完整性。

## Keywords Explanation / 關鍵字解釋

- **Attack Type** / 攻擊類型
  - DoS (Denial of Service) / 服務阻斷
  - Probe (Network probing) / 探測
  - R2L (Remote to Local) / 遠端操作
  - U2R (User to Root) / 使用者權限提升
- Intrusion Detection System (IDS) / 入侵偵測系統

## References / 參考資料

- [A Detailed Analysis of the KDD CUP 99 Data Set](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5356528)
- [入侵檢測數據集](https://blog.csdn.net/HuTingyu/article/details/106479473)
- [快速了解 NSL-KDD 数据集](https://blog.csdn.net/airenKKK/article/details/124619217)
- [針對未知攻擊辨識之混合式入侵檢測系統](https://ir.nctu.edu.tw/bitstream/11536/76169/1/608301.pdf)
