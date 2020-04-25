# Why??

我為什麼會做這個專案呢? 其實只是為了證明下面文章中所討論的作業是可能的，
即使是大一學生。

 - https://bangqu.com/Ea8W71.html

# Test

server/stupid_server.py 是很簡單，而且很蠢的 server 端實作。雖然雖很笨，
但足以用來作為 PoC 或是當成作業的一部分。這個實作目前只支援兩個使用者，
一個叫 user1，另一個為 user2。他們的 password 分別為 user1_123 和
user2_123，寫死在程式碼裡。

client/stupid_client.py 是一個很蠢的 client 端實作，把 webcam 的影像傳
到 server 端。

測試步驟:
 - python server/stupid_server.py
   - 在 8001 埠提供服務
 - python client/stupid_client.py SERVER_IP 8001 user1 user1_123 
   - 以 user1 的身份連上 server
 - python client/stupid_client.py SERVER_IP 8001 user2 user2_123 
   - 以 user2 的身份連上 server

這測試流程裡，你會看到兩個視窗。每個視窗裡，同時會看到兩個獨立的影像,
來自 user1 和 user2。

然而，這個測試可能會卡住。原因是，兩個 client 都要使用 webcam，但你的
裝置上只有一個 webcam。所以你最好是分別在不同機器上執行 client。但，你
也可以改用測試用的影片取代 webcam。

使用測試影片做測試之前，必需先修改 client/gstclient.py 這個檔案。在
GstClient._build_upload() 這個 function 裡，找到 videotestsrc 這一行。
然後移除註解符號，並把 v4l2src 加上註解符號。

# 這個作業適合大一生嗎?

這個作業最大的爭議是其難道太高，大一生可能無法實作。要實作一個 video
chatroom，至少需要知道如何從 webcam 抓取影像，截取桌面的影像，並將影像
傳到 server 和傳回來。大家都覺的這很難，也確實很難。但作業本身容許使用
第三方專案，但必需有 source code。而事實上，我們已有很強的 open source
library，可以代勞這些困難的地方。學生不用從頭做起。

根據作業的需求，所有第三方程式碼必需以原始碼的形式使用，不能直接使用編
譯好的二進位 shared library 或 DLL。這意謂，學生必需從原始程式編譯成
libary，然後和主程式 link。這對 gstreamer這樣的 library 並不果難，特別
是在 Linux環境。但在 Windows，其難度可能較高。但，網路上有許多這類的文
件，應該不成問題。而且，Windows 上應該也有原生的類似專案可以使用。

# 大一生怎麼會知道這些資訊?

對於剛學習軟體相關知識的學生，確實難以知道這些元件。這也就是助教(TA)的
用處了。助教們應該協助學生，分享相關的資訊。甚至學生解釋這些 library的
一些基本概念。

以 gstreamer為例，助教應該解釋 pipeline 的功用，示範如何使用和建立
pipeline，並提供範例。這樣的分享課程不會花太多時間，我猜測在一小時之內。

# 確實發現一些困難

Threading! 大一學生應該不瞭解 multi-threading 和 async tasks。在以
gstreamer 為例，助教需要提供實際能執行的範例，讓學生知道如何把他們的
I/O 和 glib 的 event loop 整合在一起。

再以 gstreamer 為例，在程式執行當中，動態修改 pipeline 需要一些技巧。
同樣的，也需要助教提供可執行的範例。

# 結論

整體而言，這是一個很好的大一（下）作業，雖然有些挑戰。雖然他們在知識和
經驗上不足，但助教們能提供幫助，提供相關的資訊，補足這些知識。而且學生
們會互相幫助，或找尋可用資源。這個作業最棒的地方是讓學生學習利用和整合
別人的專案，團隊合作，和尋找幫助。

