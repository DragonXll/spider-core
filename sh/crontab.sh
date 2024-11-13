##/var/spool/cron/
## crontab -e
#zz-废气
20 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 3 1
5 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 3 2
5 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 3 3
5 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 3 4
#zz-废气voc
21 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 4 1
10 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 4 2
10 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 4 3
10 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 4 4
#ls-废气
22 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 3 1
15 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 3 2
15 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 3 3
15 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 3 4
#ls-废水
24 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 5 1
20 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 5 2
20 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 5 3
20 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 5 4
#ls-污水厂
25 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 6 1
25 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 6 2
25 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 6 3
25 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 6 4
#ls-自行监测
26 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 7 1
30 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 7 2
30 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 7 3
30 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 7 4
#ls-出租车走航【道路】
30 8 * * * sh /usr/local/runJar/spider-core/sh/start_air.sh ls 1 1
#崂山-企业用电
0 16 * * * sh /usr/local/runJar/spider-core/sh/start_elec.sh
#崂山-餐饮小时数据
*/10 * * * * sh /usr/local/runJar/spider-core/sh/start_air.sh ls 2 1
#崂山-餐饮数据【新】
*/10 * * * * sh /usr/local/runJar/spider-core/sh/start_air.sh ls 5 1
#崂山-餐饮超标数据
0 0 */1 * * sh /usr/local/runJar/spider-core/sh/start_air.sh ls 3 2
#ls-渣土车-违规记录
20 8 * * * sh /usr/local/runJar/spider-core/sh/start_air.sh ls 4
#通用-大气分析计算
*/5 * * * * sh /usr/local/runJar/spider-core/sh/start_analy.sh 1
*/5 * * * * sh /usr/local/runJar/spider-core/sh/start_analy.sh 2
#危固废联单
0 * * * * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 1 1
0 * * * * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 1 2
0 * * * * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 1 3
#危固废经营报告
0 0 1 * * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 2 1
0 0 1 1 * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 2 2
0 0 1 1 * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 2 3

