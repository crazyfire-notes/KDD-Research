# KDD-Research

This repo is for KDD Dataset Research and Any kinds of Related works.

## What is NSL-KDD Dataset? / 什麼是 NSL-KDD Dataset?

- NSL-KDD Dataset 是 KDD'99 Dataset 的修訂版本，並解決了
  - KDD'99 Dataset 中有冗余資料的問題。
  - KDD'99 Dataset 中的測試集有來自訓練集的資料副本的問題。
  -

## The History of NSL-KDD Dataset / NSL-KDD Dataset 的歷史

- NSL-KDD Dataset 是在 2009 年由 UNB (University of New Brunswick) 所整理開發的，旨在解決於 1999 年 KDD Cup 中所使用的 KDD'99 Dataset 中的問題。
- KDD'99 Dataset 則是在 1999 使用在 KDD Cup 1999 年的 計算機網路入侵偵測競賽 中的資料集，由 Stolfo 等人所整理，其數據源自於 1998 年 DARPA (Defense Advanced Research Projects Agency) 所紀錄的 9 週的網路流量，並依照前七週的數據作為訓練集，後兩週的數據作為測試集。
- 而 DARPA 98 則是由 MIT Lincoln Lab 所提供的，其創建目的為調查和評估入侵檢測研究。此環境模擬了典型美國空軍 LAN 的九週原始 TCP 轉存數據，在將此 LAN 視為真正的空軍環境做操作的過程中，也同時對其進行攻擊。
  - 此還環境所遭受的攻擊主要分成四大類：
    - DoS (Denial of Service)：拒絕服務攻擊，主要是透過洪水攻擊 (Flood Attack) 來使目標主機或網路資源無法提供正常的服務。
    - Probe：探查攻擊，主要是透過探查來找出目標主機或網路資源的弱點。
    - R2L (Remote to Local)：遠端到本地攻擊，主要是透過遠端的方式來攻擊本地主機或網路資源。
    - U2R (User to Root)：使用者到高權限使用者攻擊，主要是透過嘗試提升使用者權限來攻擊本地主機或網路資源。
  - 更重要的事情是測試資料中跟訓練資料是有所落差的，在測試資料中有完全不包含在訓練資料中的特定攻擊類型，而且在測試資料中的攻擊類型的比例也與訓練資料中的攻擊類型的比例不同。
    > 此部分讓很多專家認為更貼近真實環境，因為在真實環境中，攻擊者會不斷地創造新的攻擊方式，而且攻擊的比例也會隨著時間的推移而改變。
- 總結：
  - KDD'99 由於是 DARPA 98 的整理版本，因此在攻擊類型上當然是看齊 DARPA 98 的攻擊類型，也分成了四大類。NSL-KDD 又是 KDD'99 的修訂版本，因此也是此四大類攻擊特徵。

## The difference of KDD Data set / KDD Data set 的差異

- KDD 相比一般對於網路流量的收集，提供了共 43 種數據特徵，包含 41 個原始數據特徵，跟一個攻擊類型標籤，以及一個攻擊嚴重性標籤。
- 在 41 種特徵中，又可以分成三大類型，分別是

  - 基礎連線特徵，也就是我們常見關於流量的資訊內容，包含
    1. duration: 連線持續時間
    2. protocol_type: 連線協定
    3. service: 目標主機的服務類型 (所連線的服務)
    4. flag: 連線是否正常或錯誤 (連線狀態)
    5. src_bytes: 來源端傳送到目的端的 bytes 數量
    6. dst_bytes: 目的端傳送到來源端的 bytes 數量
    7. land: 來源端跟目的端是否為同一個 IP 跟 Port
    8. wrong_fragment: 連線中的錯誤片段數量
    9. urgent: 連線中的 urgent 封包數量 (也就是在 packet 中有 urgent bit 的 packet 數量)
  - 連線內容特徵，也就是對於服務的操作互動上的特徵，包含
    1. hot: 連線中的訪問敏感服務/資源的次數
    2. num_failed_logins: 連線中的登入失敗次數
    3. logged_in: 連線中是否有登入成功
    4. num_compromised: 連線中的有多少"被入侵的目標" (compromise indicator) Number of "compromised" conditions
       > 不確定該如何翻譯跟理解
    5. root_shell: 連線中是否有 root shell (root 用戶權限的指令)
    6. su_attempted: 連線中是否有 `su` 指令的使用
    7. num_root (number of "root" accesses): 連線中有多少次 root 權限的操作
    8. num_file_creations (number of file creation operations): 連線中有多少次建立檔案的操作
    9. num_shells (number of shells): Shell 被開啟的次數
    10. num_access_files (number of operations on access control files): 連線中有多少次對 access control files 的操作
    11. num_outbound_cmds (number of outbound commands in an ftp session): 連線中有多少次對 ftp session 的 outbound 指令
    12. is_host_login (is this login a host (not a user) login): 連線中是否有 host login
    13. is_guest_login (is this login a "guest" login): 連線中是否有 guest login
  - 基於時間的特徵，也就是對於連線的時間上的特徵，包含
    1. count: 連線的次數
    2. srv_count: 連線的次數 (server)
    3. serror_rate: 連線中的錯誤封包數量 / 連線中的封包數量
    4. srv_serror_rate: 連線中的錯誤封包數量 / 連線中的封包數量 (server)
    5. rerror_rate: 連線中的錯誤回應數量 / 連線中的回應數量
    6. srv_rerror_rate: 連線中的錯誤回應數量 / 連線中的回應數量 (server)
    7. same_srv_rate: 連線中的相同服務的封包數量 / 連線中的封包數量
    8. diff_srv_rate: 連線中的不同服務的封包數量 / 連線中的封包數量
    9. srv_diff_host_rate: 連線中的不同主機的封包數量 / 連線中的封包數量 (server)
  - 基於主機的特徵，也就是對於連線的主機上的特徵，包含
    1.  dst_host_count: 連線中的目的主機數量
    2.  dst_host_srv_count: 連線中的目的主機數量 (server)
    3.  dst_host_same_srv_rate: 連線中的相同服務的封包數量 / 連線中的封包數量 (目的主機)
    4.  dst_host_diff_srv_rate: 連線中的不同服務的封包數量 / 連線
    5.  dst_host_same_src_port_rate: 連線中的相同來源端口的封包數量 / 連線中的封包數量 (目的主機)
    6.  dst_host_srv_diff_host_rate: 連線中的不同主機的封包數量 / 連線中的封包數量 (目的主機)
    7.  dst_host_serror_rate: 連線中的錯誤封包數量 / 連線中的封包數量 (目的主機)
    8.  dst_host_srv_serror_rate: 連線中的錯誤封包數量 / 連線中的封包數量 (目的主機 server)
    9.  dst_host_rerror_rate: 連線中的錯誤回應數量 / 連線中的回應數量 (目的主機)
    10. dst_host_srv_rerror_rate: 連線中的錯誤回應數量 / 連線中的回應數量 (目的主機 server)
  - 最後則是標籤跟等級，包含
    1.  class: 連線的類別，是 `normal` (正常) 還是 `anomaly` (異常)
    2.  difficulty_level: 連線的難度等級

- 依照這樣去對資料做細分是有意義的，
  - 首先是 "封包基本連線特徵"，這很好理解，本來 Traffic 中就會有這些資訊，而且理論上互動上來說怎樣才算是 "符合預期" 在這個領域上是有一定的共識的，所以這部分的特徵是比較好理解的
  - 其次是 "封包內容特徵"，這部分可以算是對於 R2L 跟 U2R 這兩種攻擊型態所專屬的特徵狀況，由於相較於其他兩種攻擊型態，往往會由大量且多個 packets 所組成，R2L 跟 U2R 往往只有一個 packet 所攜帶的 payload 就屬於一個操作了，所以歸納了這類型的特徵。
  - 再來是對於連續封包的特徵，分別有 "基於時間" 跟 "基於同服務" 
