# Podcast backup from RSS/libsyn

Downloads from Libsyn or similar sites based on their RSS feed.
* Quality as-is, very basic script.
* Presumes you want the following directory structure:
  * `dir/rss.xml`
  * `dir/YYY/MM/YYYYMMDD_title/filename.mp3`

## Usage

Try `python3 podcast.backup.py -h` for help!

```
usage: podcast.backup.py [-h] --dir DIR --url URL [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Libsyn RSS to Mp3 backup (alpha quality)

options:
  -h, --help            show this help message and exit
  --dir DIR             Directory to backup to. Writes files to dir/YYYY/MM/YYYYMMDD_Title/name.mp3
  --url URL             URL to lib-syn RSS feed, e.g. https://sakerhetspodcasten.libsyn.com/rss
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}

Hope this help was helpful! :-)
```

Example: `python3 podcast.backup.py --dir test --url https://sakerhetspodcasten.libsyn.com/rss`

```
2023-04-02 19:19:42,839 INFO Request feed from https://sakerhetspodcasten.libsyn.com/rss
2023-04-02 19:19:54,264 INFO Parse test/rss.xml
2023-04-02 19:19:54,436 INFO 254 files processed.
2023-04-02 19:19:54,436 INFO 254 files skipped; allready downloaded.
2023-04-02 19:19:54,436 INFO 0 files downloaded.
```

Example: `python3 podcast.backup.py --dir test --url https://sakerhetspodcasten.libsyn.com/rss --loglevel DEBUG`

```
2023-04-02 18:57:03,405 INFO Request feed from https://sakerhetspodcasten.libsyn.com/rss
2023-04-02 18:57:13,457 DEBUG Download: test/2023/03/20230327_sakerhetspodcasten_237_jobba_i_sakerhetsbranschen/2023_02_22_jobb_i_sakbranchen.mp3 : Allready downloaded.
2023-04-02 18:57:13,457 DEBUG Download: test/2023/03/20230320_sakerhetspodcasten_236_ostrukturerat_v_12/2023_03_15_sakerhetspodcasten.mp3 : Allready downloaded.
2023-04-02 18:57:13,458 DEBUG Download: test/2023/02/20230227_sakerhetspodcasten_235_ostrukturerat_v_9/2023_02_22_skerhetspodcasten.mp3 : Allready downloaded.
2023-04-02 18:57:13,458 DEBUG Download: test/2023/02/20230206_sakerhetspodcasten_234_nyar_2022/2023_01_18_nyr2022.mp3 : Allready downloaded.
2023-04-02 18:57:13,458 DEBUG Download: test/2023/01/20230121_sakerhetspodcasten_233_ostrukturerat_v_3/2023_01_18_sakpodcasten_ostrukt.mp3 : Allready downloaded.
2023-04-02 18:57:13,458 DEBUG Download: test/2023/01/20230109_sakerhetspodcasten_232_jul_2022/2022_12_13_xmas.mp3 : Allready downloaded.
2023-04-02 18:57:13,458 DEBUG Download: test/2022/12/20221219_sakerhetspodcasten_231_ostrukturerat_v_51/2022_12_13_skerhetspodcasten.mp3 : Allready downloaded.
2023-04-02 18:57:13,459 DEBUG Download: test/2022/11/20221128_sakerhetspodcasten_230_testa_nya_saker/2022_11_09_testanytt.mp3 : Allready downloaded.
2023-04-02 18:57:13,459 DEBUG Download: test/2022/11/20221114_sakerhetspodcasten_229_ostrukturerat_v_46/2022_11_09_skerhetspodcasten.mp3 : Allready downloaded.
2023-04-02 18:57:13,459 DEBUG Download: test/2022/10/20221031_sakerhetspodcasten_228_sec_t_community_night_2022/2022_09_14_sec_t_community_night_intervjuer.mp3 : Allready downloaded.
2023-04-02 18:57:13,459 DEBUG Download: test/2022/10/20221017_sakerhetspodcasten_227_ostrukturerat_v_42/2022_10_12_sakerhetspodcasten.mp3 : Allready downloaded.
2023-04-02 18:57:13,459 DEBUG Download: test/2022/07/20220707_sakerhetspodcasten_226_riskanalys/2022_06_15_risk_analys.mp3 : Allready downloaded.
2023-04-02 18:57:13,459 DEBUG Download: test/2022/06/20220620_sakerhetspodcasten_225_ostrukturerat_v_25/2022_06_15_ostrukturerat.mp3 : Allready downloaded.
...
```
