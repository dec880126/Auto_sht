<h1 align="center">Auto SHT</h1>

To simplify the work for browsing sehuatang.org

## Necessary modules
Of course ``Python environment`` is necessary.<br>
In addition to environment, the modules below are also necessary.
```
pip install requests 
pip install beautifulsoup4
pip install datetime
pip install pyperclip
```

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
|ver 4.1.0  |更改    |增加整體程式碼可讀性
|ver 4.2.0  |新增    |config.ini配置檔案

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

