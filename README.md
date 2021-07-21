<h1 align="center">Auto SHT</h1>

高速瀏覽並抓取 sehuatang.org 的 magnet 之解決方案 by Python3<br>
## Single-Threading 與 Multi-Threading 之效能比較
圖為於v5.0.0 版本更動中加入之 Multi-Threading 與舊版之 Single-Threading 之效能比較
整體速度平均提升了約 **5.2** 倍<br>
> 縱軸為抓取所花費之時間 單位:秒(sec)<br>
> 橫軸為抓取之文章數量<br>

![1626855450079](https://user-images.githubusercontent.com/34447298/126466711-6dc99eb8-0894-4342-8079-d1ad9a1a2e96.jpg)

## Development Notes

|           |  Type  |What's New                        
|-----------|--------|--------------------------
|ver 1.0.0  |初版    |magnet 之 sehuatang 輔助程式
|ver 1.1.0  |新增    |挑出當日更新文章功能      
|ver 1.2.0  |新增    |提取文章標題功能
|ver 1.3.0  |新增    |預覽圖連結提取功能
|ver 1.3.1  |優化    |Optimization and Bug fixes
|ver 1.4.0  |新增    |抓取之日期選擇與修改功能
|ver 1.5.0  |新增    |圖片預覽 HTML file 產生功能
|ver 1.5.1  |優化    |Optimization and Bug fixes
|ver 1.5.2  |優化    |Optimization and Bug fixes
|ver 1.5.3  |優化    |抓取進度視覺化
|ver 1.6.0  |新增    |多頁搜尋功能
|ver 1.6.1  |優化    |Optimization and Bug fixes
|ver 1.6.2  |優化    |日期選擇功能
|ver 1.6.3  |優化    |文章清單抓取效能
|ver 1.6.4  |優化    |資料抓取具暫存功能
|ver 2.0.0  |架構更動|導入物件導向系統
|ver 3.0.0  |新增    |挑選功能
|ver 3.1.0  |新增    |自動開啟產生之HTML files
|ver 3.2.0  |優化    |資料抓取效能 速度提升約 3 倍
|ver 3.2.1  |修正    |Bug fixes: 中文區 偶爾會出現沒無 magnet 連結，只有 `.torrent` 的報錯修正
|ver 3.3.0  |優化    |HTML files 分頁顯示
|ver 3.4.0  |新增    |已搜尋過之 magnet 查詢功能
|ver 3.5.0  |新增    |資料重置功能
|ver 3.5.1  |修正    |Bug fixes: 解決當日無更新文章會崩潰的錯誤
|ver 3.6.0  |優化    |1. HTML files 美化以及新增標題及 magnet 預覽功能<br>2. 連結至 sehuatang.org 之 link
|ver 3.7.0  |新增    |提取之 magnet 清單自動導入剪貼簿
|ver 3.8.0  |新增    |選擇過程中如果按錯誤刪，現在提供返回修正機制
|ver 3.8.1  |修正    |Bug fixes: 修正連續抓取失敗問題
|ver 3.8.2  |優化    |程式報錯畫面優化
|ver 3.8.3  |修正    |Bug fixes: 修正返回機制崩潰問題
|ver 3.8.4  |優化    |HTML files 產生邏輯與 HTML files 刪除機制優化
|ver 3.8.5  |新增    |自動檢查更新功能
|ver 3.8.6  |修正    |Bug fixes: 修正 magnet 顯示錯誤問題
|ver 3.8.7  |優化    |提升進度條準確性
|ver 4.0.0  |新增    |串接 Synology API 系統，可實現自動加入任務至 Download Station
|ver 4.0.1  |優化    |可在輸入 Synology 密碼時畫面隱藏
|ver 4.1.0  |更改    |改善整體程式碼可讀性
|ver 4.2.0  |新增    |config.ini配置檔案
|ver 4.3.0  |新增    |有碼區自動挑除素人系列功能
|ver 5.0.0  |架構更動|使用多執行緒 (Multi-Threading) 來執行抓取作業，大幅提升了作業效率
|ver 5.0.1  |修正    |修正連續抓取失敗問題 以及 優化沒選擇 magnet 的狀況下之程式流程
|ver 5.0.2  |優化    |優化 HTML files 刪除邏輯
|ver 5.0.3  |優化    |優化主程式之強制中斷流程


## Config.ini 配置方法
### upload
> 若要開啟 Synology 自動上傳，將 upload 設為1 否則為0 <br>
### IP
> Synology NAS 之 IP<br>
### PORT
> Synology NAS 之 PORT<br>
### PATH
> BT 下載之路徑<br>
### SECURE
> 加密傳輸，預設是在區網內使用為0，否則為1<br>
### USER
> Synology NAS 之 Account<br>
### PASSWORD
> Synology NAS 之 Password<br>

## How to use?
- By .exe
	1. Click `Auto_sht.exe`
	2. Running
	
- By .bat
	1. Download the latest release
	2. UNZIP
	3. click the `auto_sht.bat`

- By Python Compiler
> Windows User<br>
	1. Open the cmd.exe or Windows PowerShell at the folder where `auto_sht.py` is<br>
	2. type the command `python .\auto_sht.py`<br>
	
PS: Recommend using **Windows PowerShell** rather then **CMD.exe**

> Mac OS User<br>
	1. Open the Terminal at the folder where `auto_sht.py` is<br>
	2. type the command `python .\auto_sht.py`

