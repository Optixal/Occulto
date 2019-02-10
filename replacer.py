#!/usr/bin/env python3
import re

replacements = {
    b'yahoo.com'               : b'\x00' , # 0   : 1942758
    b'hotmail.com'             : b'\x01' , # 1   : 1018430
    b'mail.ru'                 : b'\x02' , # 2   : 998499
    b'gmail.com'               : b'\x03' , # 3   : 919974
    b'aol.com'                 : b'\x04' , # 4   : 320558
    b'yandex.ru'               : b'\x05' , # 5   : 158110
    b'yahoo.com.vn'            : b'\x06' , # 6   : 133011
    b'hotmail.it'              : b'\x07' , # 7   : 83939
    b'bk.ru'                   : b'\x08' , # 8   : 83333
    b'live.com'                : b'\t'   , # 9   : 81100
    b'hotmail.co.uk'           : b'\n'   , # 10  : 77553
    b'westpost.net'            : b'\x0b' , # 11  : 73137
    b'web.de'                  : b'\x0c' , # 12  : 61581
    b'comcast.net'             : b'\r'   , # 13  : 60867
    b'msn.com'                 : b'\x0e' , # 14  : 55873
    b'list.ru'                 : b'\x0f' , # 15  : 47446
    b'inbox.ru'                : b'\x10' , # 16  : 45739
    b'yahoo.co.uk'             : b'\x11' , # 17  : 45499
    b'rambler.ru'              : b'\x12' , # 18  : 43545
    b'aim.com'                 : b'\x13' , # 19  : 41970
    b'free.fr'                 : b'\x14' , # 20  : 37090
    b'gmx.de'                  : b'\x15' , # 21  : 37078
    b'sbcglobal.net'           : b'\x16' , # 22  : 35895
    b'live.it'                 : b'\x17' , # 23  : 35344
    b'hotmail.fr'              : b'\x18' , # 24  : 33272
    b'libero.it'               : b'\x19' , # 25  : 28775
    b'ymail.com'               : b'\x1a' , # 26  : 25661
    b'verizon.net'             : b'\x1b' , # 27  : 20905
    b'wanadoo.fr'              : b'\x1c' , # 28  : 19591
    b'wp.pl'                   : b'\x1d' , # 29  : 19248
    b'yahoo.co.in'             : b'\x1e' , # 30  : 18145
    b'orange.fr'               : b'\x1f' , # 31  : 17990
    b'rediffmail.com'          : b' '    , # 32  : 17946
    b'cox.net'                 : b'!'    , # 33  : 17847
    b'yahoo.it'                : b'"'    , # 34  : 17226
    b'yahoo.de'                : b'#'    , # 35  : 16921
    b'hotmail.de'              : b'$'    , # 36  : 16878
    b'myspace.com'             : b'%'    , # 37  : 16285
    b'mail.com'                : b'&'    , # 38  : 15692
    b'att.net'                 : b"'"    , # 39  : 15054
    b'bellsouth.net'           : b'('    , # 40  : 14972
    b'earthlink.net'           : b')'    , # 41  : 14438
    b'googlemail.com'          : b'*'    , # 42  : 13697
    b'o2.pl'                   : b'+'    , # 43  : 13577
    b'rocketmail.com'          : b','    , # 44  : 13471
    b'alice.it'                : b'-'    , # 45  : 13412
    b'freenet.de'              : b'.'    , # 46  : 13383
    b't-online.de'             : b'/'    , # 47  : 12724
    b'live.co.uk'              : b'0'    , # 48  : 12498
    b'yahoo.fr'                : b'1'    , # 49  : 12256
    b'outlook.com'             : b'2'    , # 50  : 12114
    b'tiscali.it'              : b'3'    , # 51  : 12097
    b'gmx.net'                 : b'4'    , # 52  : 11334
    b'qip.ru'                  : b'5'    , # 53  : 11073
    b'yahoo.com.br'            : b'6'    , # 54  : 10811
    b'btinternet.com'          : b'7'    , # 55  : 10800
    b'seznam.cz'               : b'8'    , # 56  : 10421
    b'charter.net'             : b'9'    , # 57  : 9794
    b'interia.pl'              : b':'    , # 58  : 9654
    b'sina.com'                : b';'    , # 59  : 9135
    b'mac.com'                 : b'<'    , # 60  : 9043
    b'ntlworld.com'            : b'='    , # 61  : 8984
    b'ukr.net'                 : b'>'    , # 62  : 8849
    b'numericable.fr'          : b'?'    , # 63  : 7925
    b'mail.ua'                 : b'@'    , # 64  : 7798
    b'zing.vn'                 : b'A'    , # 65  : 7675
    b'ya.ru'                   : b'B'    , # 66  : 7616
    b'myemailboxmail.com'      : b'C'    , # 67  : 7582
    b'juno.com'                : b'D'    , # 68  : 7417
    b'freelymail.com'          : b'E'    , # 69  : 7188
    b'yahoo.ca'                : b'F'    , # 70  : 7028
    b'freemailmail.com'        : b'G'    , # 71  : 7013
    b'inbox.lv'                : b'H'    , # 72  : 6570
    b'gmx.at'                  : b'I'    , # 73  : 6344
    b'live.fr'                 : b'J'    , # 74  : 6084
    b'freemailboxy.com'        : b'K'    , # 75  : 6072
    b'optonline.net'           : b'L'    , # 76  : 5982
    b'excite.com'              : b'M'    , # 77  : 5981
    b'163.com'                 : b'N'    , # 78  : 5876
    b'usa.net'                 : b'O'    , # 79  : 5730
    b'yahoo.com.au'            : b'P'    , # 80  : 5660
    b'arcor.de'                : b'Q'    , # 81  : 5590
    b'yahoo.com.tw'            : b'R'    , # 82  : 5426
    b'email.com'               : b'S'    , # 83  : 5251
    b'yahoo.es'                : b'T'    , # 84  : 5176
    b'hotmail.es'              : b'U'    , # 85  : 4976
    b'tiscali.co.uk'           : b'V'    , # 86  : 4966
    b'home.com'                : b'W'    , # 87  : 4891
    b'abv.bg'                  : b'X'    , # 88  : 4841
    b'vipmail.net'             : b'Y'    , # 89  : 4772
    b'nowemailbox.com'         : b'Z'    , # 90  : 4768
    b'me.com'                  : b'['    , # 91  : 4723
    b'hotmailboxlive.com'      : b'\\'   , # 92  : 4678
    b'live.nl'                 : b']'    , # 93  : 4492
    b'virgilio.it'             : b'^'    , # 94  : 4453
    b'anonemailbox.com'        : b'_'    , # 95  : 4443
    b'op.pl'                   : b'`'    , # 96  : 4368
    b'netscape.net'            : b'a'    , # 97  : 4278
    b'yahoo.com.mx'            : b'b'    , # 98  : 4117
    b'live.de'                 : b'c'    , # 99  : 4063
    b'uol.com.br'              : b'd'    , # 100 : 3782
    b'yahoo.com.uk'            : b'e'    , # 101 : 3732
    b'yahoo.com.hk'            : b'f'    , # 102 : 3725
    b'cs.com'                  : b'g'    , # 103 : 3712
    b'blueyonder.co.uk'        : b'h'    , # 104 : 3699
    b'telenet.be'              : b'i'    , # 105 : 3646
    b'myemailmail.com'         : b'j'    , # 106 : 3641
    b'live.com.au'             : b'k'    , # 107 : 3616
    b'bol.com.br'              : b'l'    , # 108 : 3611
    b'lycos.com'               : b'm'    , # 109 : 3591
    b'bigmir.net'              : b'n'    , # 110 : 3571
    b'netzero.net'             : b'o'    , # 111 : 3533
    b'tom.com'                 : b'p'    , # 112 : 3528
    b'gmail.ru'                : b'q'    , # 113 : 3494
    b'live.ca'                 : b'r'    , # 114 : 3489
    b'tlen.pl'                 : b's'    , # 115 : 3304
    b'freemail.hu'             : b't'    , # 116 : 3289
    b'yahoo.co.jp'             : b'u'    , # 117 : 3174
    b'yandex.ua'               : b'v'    , # 118 : 3136
    b'yahoo.com.sg'            : b'w'    , # 119 : 3130
    b'yahoo.com.cn'            : b'x'    , # 120 : 3098
    b'yahoo.com.my'            : b'y'    , # 121 : 3048
    b'mindspring.com'          : b'z'    , # 122 : 3045
    b'yahoo.com.ph'            : b'{'    , # 123 : 3032
    b'shaw.ca'                 : b'|'    , # 124 : 3014
    b'myemailboxy.com'         : b'}'    , # 125 : 2990
    b'rogers.com'              : b'~'    , # 126 : 2973
    b'sympatico.ca'            : b'\x7f' , # 127 : 2957
    b'adelphia.net'            : b'\x80' , # 128 : 2956
    b'windstream.net'          : b'\x81' , # 129 : 2916
    b'onlinemailfree.com'      : b'\x82' , # 130 : 2857
    b'yahoo.com.ar'            : b'\x83' , # 131 : 2822
    b'peoplepc.com'            : b'\x84' , # 132 : 2811
    b'laposte.net'             : b'\x85' , # 133 : 2768
    b'uukx.info'               : b'\x86' , # 134 : 2753
    b'tut.by'                  : b'\x87' , # 135 : 2729
    b'bigpond.com'             : b'\x88' , # 136 : 2721
    b'naver.com'               : b'\x89' , # 137 : 2717
    b'icloud.com'              : b'\x8a' , # 138 : 2679
    b'privacymailshh.com'      : b'\x8b' , # 139 : 2673
    b'netzero.com'             : b'\x8c' , # 140 : 2649
    b'.mail.ru'                : b'\x8d' , # 141 : 2629
    b'onet.pl'                 : b'\x8e' , # 142 : 2493
    b'windowslive.com'         : b'\x8f' , # 143 : 2489
    b'gmx.com'                 : b'\x90' , # 144 : 2459
    b'yahoo.co.id'             : b'\x91' , # 145 : 2420
    b'prodigy.net'             : b'\x92' , # 146 : 2385
    b'email.it'                : b'\x93' , # 147 : 2366
    b'mailinator.com'          : b'\x94' , # 148 : 2362
    b'noos.fr'                 : b'\x95' , # 149 : 2326
    b'embarqmail.com'          : b'\x96' , # 150 : 2322
    b'i.ua'                    : b'\x97' , # 151 : 2309
    b'iol.ie'                  : b'\x98' , # 152 : 2273
    b'sky.com'                 : b'\x99' , # 153 : 2271
    b'126.com'                 : b'\x9a' , # 154 : 2245
    b'mchsi.com'               : b'\x9b' , # 155 : 2222
    b'mail.ry'                 : b'\x9c' , # 156 : 2216
    b'live.com.mx'             : b'\x9d' , # 157 : 2210
    b'sify.com'                : b'\x9e' , # 158 : 2157
    b'hotmail.com.blocked_recovery' : b'\x9f' , # 159 : 2117
    b'blackplanet.com'         : b'\xa0' , # 160 : 2103
    b'walla.com'               : b'\xa1' , # 161 : 2093
    b'vp.pl'                   : b'\xa2' , # 162 : 2085
    b'insightbb.com'           : b'\xa3' , # 163 : 2070
    b'gadball.com'             : b'\xa4' , # 164 : 2015
    b'parapa.terrhq.ru'        : b'\xa5' , # 165 : 1983
    b'tampabay.rr.com'         : b'\xa6' , # 166 : 1963
    b'optusnet.com.au'         : b'\xa7' , # 167 : 1945
    b'hanmail.net'             : b'\xa8' , # 168 : 1934
    b'hot.ee'                  : b'\xa9' , # 169 : 1924
    b'yahoo.gr'                : b'\xaa' , # 170 : 1899
    b'aliceadsl.fr'            : b'\xab' , # 171 : 1896
    b'yandex.com'              : b'\xac' , # 172 : 1894
    b'qq.com'                  : b'\xad' , # 173 : 1878
    b'us.army.mil'             : b'\xae' , # 174 : 1875
    b'tmail.com'               : b'\xaf' , # 175 : 1869
    b'suddenlink.net'          : b'\xb0' , # 176 : 1853
    b'myway.com'               : b'\xb1' , # 177 : 1837
    b'ig.com.br'               : b'\xb2' , # 178 : 1796
    b'one.lv'                  : b'\xb3' , # 179 : 1733
    b'roadrunner.com'          : b'\xb4' , # 180 : 1726
    b'gmx.ch'                  : b'\xb5' , # 181 : 1719
    b'indiatimes.com'          : b'\xb6' , # 182 : 1689
    b'homechoice.co.uk'        : b'\xb7' , # 183 : 1687
    b'mai.ru'                  : b'\xb8' , # 184 : 1675
    b'altavista.com'           : b'\xb9' , # 185 : 1647
    b'yhaoo.com'               : b'\xba' , # 186 : 1626
    b'neuf.fr'                 : b'\xbb' , # 187 : 1600
    b'centrum.cz'              : b'\xbc' , # 188 : 1578
    b'live.se'                 : b'\xbd' , # 189 : 1575
    b'poczta.onet.pl'          : b'\xbe' , # 190 : 1556
    b'inbox.com'               : b'\xbf' , # 191 : 1551
    b'online.de'               : b'\xc0' , # 192 : 1543
    b'pacbell.net'             : b'\xc1' , # 193 : 1542
    b'cfl.rr.com'              : b'\xc2' , # 194 : 1541
    b'maii.ru'                 : b'\xc3' , # 195 : 1534
    b'frontiernet.net'         : b'\xc4' , # 196 : 1532
    b'worldnet.att.net'        : b'\xc5' , # 197 : 1528
    b'go2.pl'                  : b'\xc6' , # 198 : 1527
    b'bluewin.ch'              : b'\xc7' , # 199 : 1524
    b'gci.net'                 : b'\xc8' , # 200 : 1512
    b'sibmail.com'             : b'\xc9' , # 201 : 1474
    b'telus.net'               : b'\xca' , # 202 : 1471
    b'meta.ua'                 : b'\xcb' , # 203 : 1469
    b'citromail.hu'            : b'\xcc' , # 204 : 1452
    b'tin.it'                  : b'\xcd' , # 205 : 1437
    b'orsk.ru'                 : b'\xce' , # 206 : 1433
    b'modulonet.fr'            : b'\xcf' , # 207 : 1413
    b'gmx.co.uk'               : b'\xd0' , # 208 : 1411
    b'fastwebnet.it'           : b'\xd1' , # 209 : 1399
    b'email.cz'                : b'\xd2' , # 210 : 1399
    b'talktalk.net'            : b'\xd3' , # 211 : 1396
    b'webtv.net'               : b'\xd4' , # 212 : 1353
    b'yahoo.in'                : b'\xd5' , # 213 : 1345
    b'google.com'              : b'\xd6' , # 214 : 1332
    b'interia.eu'              : b'\xd7' , # 215 : 1319
    b'virgin.net'              : b'\xd8' , # 216 : 1311
    b'onebox.com'              : b'\xd9' , # 217 : 1310
    b'onet.eu'                 : b'\xda' , # 218 : 1289
    b'yaho.com'                : b'\xdb' , # 219 : 1246
    b'mynet.com'               : b'\xdc' , # 220 : 1245
    b'usa.com'                 : b'\xdd' , # 221 : 1245
    b'mail.bg'                 : b'\xde' , # 222 : 1237
    b'pochta.ru'               : b'\xdf' , # 223 : 1219
    b'hotmail.ca'              : b'\xe0' , # 224 : 1202
    b'azet.sk'                 : b'\xe1' , # 225 : 1188
    b'mailcity.com'            : b'\xe2' , # 226 : 1155
    b'sfr.fr'                  : b'\xe3' , # 227 : 1150
    b'comcast.com'             : b'\xe4' , # 228 : 1145
    b'caramail.com'            : b'\xe5' , # 229 : 1139
    b'poczta.fm'               : b'\xe6' , # 230 : 1125
    b'gawab.com'               : b'\xe7' , # 231 : 1123
    b'terra.com.br'            : b'\xe8' , # 232 : 1119
    b'nate.com'                : b'\xe9' , # 233 : 1118
    b'aon.at'                  : b'\xea' , # 234 : 1113
    b'catcha.com'              : b'\xeb' , # 235 : 1112
    b'yopmail.com'             : b'\xec' , # 236 : 1101
    b'bigpond.net.au'          : b'\xed' , # 237 : 1090
    b'home.nl'                 : b'\xee' , # 238 : 1085
    b'yhoo.com'                : b'\xef' , # 239 : 1082
    b'elance.com'              : b'\xf0' , # 240 : 1079
    b'btopenworld.com'         : b'\xf1' , # 241 : 1068
    b'alltel.net'              : b'\xf2' , # 242 : 1067
    b'q.com'                   : b'\xf3' , # 243 : 1065
    b'classgess.com'           : b'\xf4' , # 244 : 1036
    b'dabjam.com'              : b'\xf5' , # 245 : 1028
    b'bigfoot.com'             : b'\xf6' , # 246 : 1025
    b'mediaone.net'            : b'\xf7' , # 247 : 1024
    b'cableone.net'            : b'\xf8' , # 248 : 1023
    b'yeah.net'                : b'\xf9' , # 249 : 1013
    b'verizon.com'             : b'\xfa' , # 250 : 1012
    b'astramail.bizland.com'   : b'\xfb' , # 251 : 1008
    b'centrum.sk'              : b'\xfc' , # 252 : 996
    b'fsmail.net'              : b'\xfd' , # 253 : 986
    b'rediff.com'              : b'\xfe' , # 254 : 986
    b'live.dk'                 : b'\xff' , # 255 : 984
}

inverseReplacements = {v: k for k, v in replacements.items()}

regexpReplacements = re.compile(b'(@)(' + b'|'.join(map(re.escape, replacements.keys())) + b')$')
def compress(text):
    return regexpReplacements.sub(lambda match: b'@' + replacements[match.group(2)], text)

regexpInverse = re.compile(b'(@)(' + b'|'.join(map(re.escape, inverseReplacements.keys())) + b')$')
def uncompress(text):
    return regexpInverse.sub(lambda match: b'@' + inverseReplacements[match.group(2)], text)

if __name__ == '__main__':
    print(compress(b'hello@live.com.pl'))
    print(compress(b'test@gmail.com'))
    print(compress(b'hax0r.mail.ru@mail.ru'))
