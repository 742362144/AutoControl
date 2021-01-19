import os
import subprocess

import docker
import json
from util.util import calculate_cpu_percent
import time
import traceback

TOTAL_MEM_USAGE = 8 * 1024 * 1024
data_size = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]


def idle():
    times = 100
    cid = start_redis()
    print('cid: %s' % cid)
    old = get_container_stat(cid)
    print('old: %s' % old)
    time.sleep(times)
    now = get_container_stat(cid)
    print('now: %s' % now)
    return (now - old) / times


YCSB_DIR = '/root/ycsb-redis'


def load_ycsb(workload):
    # load data
    runCmd(
        '%s/bin/ycsb load redis -s -P %s -p "redis.host=127.0.0.1" -p "redis.port=6379" > outputLoad.txt' % (
        YCSB_DIR, workload))


def run_ycsb(workload):
    # run
    runCmd(
        '%s/bin/ycsb run redis -s -P %s -p "redis.host=127.0.0.1" -p "redis.port=6379" > outputLoad.txt' % (
        YCSB_DIR, workload))


def set_data_size(workload, dsize):
    fieldlength = runCmdAndGetOutput("cat %s | grep fieldlength" % workload).strip().strip('=')[-1]
    fieldcount = runCmdAndGetOutput("cat %s | grep fieldcount" % workload).strip().strip('=')[-1]
    recordcount = runCmdAndGetOutput("cat %s | grep fieldcount" % workload).strip().strip('=')[-1]

    n_fieldcount = str(int(dsize / int(fieldlength)))
    n_recordcount = str(int(TOTAL_MEM_USAGE / dsize))
    print('start test datasize : %d' % dsize)
    runCmd("sed -i 's#fieldcount=%s#fieldcount=%s#g' %s " % (fieldcount, n_fieldcount, workload))
    runCmd("sed -i 's#recordcount=%s#recordcount=%s#g' %s " % (recordcount, n_recordcount, workload))

    print('start load data...., datasize %d, datacount: %s, operationcount: %d' % (dsize, n_recordcount, 100000))


def bench():
    res = {}
    CWD = os.getcwd()
    WORKLOADS_DIR = '%s/workloads' % CWD
    WORKLOAD = '%s/read' % WORKLOADS_DIR
    for i in data_size:
        set_data_size(WORKLOAD, i)
        cid = start_redis()
        load_ycsb(WORKLOAD)
        print('finish load data....')
        old = get_container_stat(cid)
        run_ycsb(WORKLOAD)
        print('start run test....')
        now = get_container_stat(cid)
        print('finish run test....')
        print(json.dumps(old))
        print(json.dumps(now))
        print('cpu_total: %s' % (str(now['cpu_usage']['total_usage'] - old['cpu_usage']['total_usage'])))
        case = []
        case.append(old)
        case.append(now)
        res[i] = case
        stop_redis()
    print(json.dumps(res))


def get_container_id():
    return runCmdAndGetOutput("docker ps -a | grep redis-test | awk  '{print $1}'")


def start_redis():
    cid = get_container_id()
    if cid:
        runCmd('docker start %s' % cid)
    else:
        cid = runCmdAndGetOutput('docker run -itd --name redis-test -p 6379:6379 redis')

    return cid.strip()


def stop_redis():
    runCmd('docker stop redis-test')
    # cid = runCmdAndGetOutput("docker ps | grep redis | awk  '{print $1}'")


def get_container_stat(id):
    # print('get_container_stat: id %s' % id)
    # print('get_container_stat: id %s' % type(id))
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    for c in client.containers.list():
        if c.id.find(id) == 0:
            cpu = c.stats(stream=False)
            return cpu['cpu_stats']

        # print(i.stats(stream=False))
        # for stat in i.stats():
        #      print(type(stat))
        #      d = json.loads(stat)
        #      print(d)
        #      print(calculate_cpu_percent(d))


# print(get_container_stat('d6412d090ae6'))
# print(idle())

bench()


#
def collect():
    res = []
    data = {"16": [{"cpu_usage": {"total_usage": 15168314695, "percpu_usage": [2855395943, 1594837184, 1611200098, 1695901269, 1524202521, 2547873831, 686475, 204247393, 2537698, 5397536, 6464960, 203513738, 456681869, 188794144, 533954551, 452295396, 217757601, 546378374, 0, 35311131, 1231390, 0, 1471034, 482180559], "usage_in_kernelmode": 9650000000, "usage_in_usermode": 4890000000}, "system_cpu_usage": 122689115540000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 22068061401, "percpu_usage": [3658994195, 2269676189, 2888660746, 2290789327, 2737839213, 3796666545, 686475, 210674917, 2815015, 11771350, 6464960, 223078589, 458625072, 355432986, 854313026, 768071106, 306606735, 686014909, 0, 55997063, 1231390, 0, 1471034, 482180559], "usage_in_kernelmode": 14160000000, "usage_in_usermode": 7020000000}, "system_cpu_usage": 122689595510000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "32": [{"cpu_usage": {"total_usage": 14680554973, "percpu_usage": [880216175, 381020063, 418593309, 389953271, 87287902, 267974356, 1770966131, 1995985458, 1056264467, 1684109583, 1856643524, 1530868844, 8970202, 12166243, 62020369, 107415588, 0, 0, 29375979, 1090583845, 17172052, 313949709, 533932, 718483971], "usage_in_kernelmode": 9490000000, "usage_in_usermode": 4620000000}, "system_cpu_usage": 122690598590000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 20671700175, "percpu_usage": [970821402, 434442332, 419087233, 390621980, 87287902, 267974356, 2827902406, 2450623812, 1464472603, 3004808983, 3059221105, 2444551366, 8970202, 12166243, 62020369, 107415588, 0, 0, 31451182, 1092643922, 89194004, 355355823, 372183391, 718483971], "usage_in_kernelmode": 13940000000, "usage_in_usermode": 6050000000}, "system_cpu_usage": 122691030890000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "64": [{"cpu_usage": {"total_usage": 16173613308, "percpu_usage": [180290425, 198194999, 374010097, 84147627, 280346003, 206934125, 2389604524, 2484265822, 1528304038, 1857451448, 1572936668, 1941629715, 300610, 32437185, 896844530, 2875246, 0, 3029567, 122010749, 25725768, 1241063440, 251468585, 436480479, 63261658], "usage_in_kernelmode": 10640000000, "usage_in_usermode": 5340000000}, "system_cpu_usage": 122692152890000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 23170627049, "percpu_usage": [456887777, 242098640, 1013560445, 543206507, 752147661, 546078529, 2661511391, 3032278016, 1870088044, 2517238375, 2435928823, 2207792808, 174677828, 63438193, 896910436, 636486785, 0, 170954570, 623141541, 37922578, 1312132466, 335939295, 532183179, 108023162], "usage_in_kernelmode": 15190000000, "usage_in_usermode": 7500000000}, "system_cpu_usage": 122692610120000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "128": [{"cpu_usage": {"total_usage": 15354815740, "percpu_usage": [1876536408, 1599757355, 2168387061, 1495682427, 1293946587, 1927513661, 196604672, 229257659, 206816808, 206557334, 81597817, 103864265, 847311571, 91899341, 800007787, 71223185, 843763369, 1170121652, 0, 96051299, 30645162, 0, 0, 17270320], "usage_in_kernelmode": 9840000000, "usage_in_usermode": 5120000000}, "system_cpu_usage": 122693661020000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 21651673215, "percpu_usage": [2603121255, 2378606227, 2358760111, 1926573809, 2014361460, 2466503591, 207926478, 613984667, 329793788, 329090965, 488508591, 407358377, 1793534991, 110306236, 800007787, 71223185, 879790800, 1301947645, 0, 495262077, 30645162, 27095693, 0, 17270320], "usage_in_kernelmode": 14040000000, "usage_in_usermode": 6980000000}, "system_cpu_usage": 122694117690000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "256": [{"cpu_usage": {"total_usage": 14518048773, "percpu_usage": [2651839675, 2360450330, 1074065339, 1532192180, 1831495133, 1447088271, 91914783, 115996308, 10297805, 138596788, 178446821, 24174969, 1009972606, 48897345, 105373430, 985050247, 8989420, 617193342, 0, 680962, 113945, 64923885, 217644920, 2650269], "usage_in_kernelmode": 9410000000, "usage_in_usermode": 4680000000}, "system_cpu_usage": 122695192160000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 21507408230, "percpu_usage": [3481756076, 3715385599, 2123183021, 2116461554, 2575435836, 2489873674, 153354230, 174822377, 52469842, 413234763, 338742283, 61422543, 1087846426, 194638927, 117542977, 1262152175, 23952185, 794395813, 0, 18019927, 113945, 92308868, 217644920, 2650269], "usage_in_kernelmode": 14150000000, "usage_in_usermode": 6750000000}, "system_cpu_usage": 122695696130000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "512": [{"cpu_usage": {"total_usage": 14107770425, "percpu_usage": [689092515, 178797218, 770557614, 308723729, 1110564762, 380605987, 875840718, 2192435061, 686709981, 1803847450, 932011402, 1985331667, 8121510, 32509749, 340895755, 3125634, 757867545, 26124293, 130419632, 211073983, 13036639, 6470570, 274211984, 389395027], "usage_in_kernelmode": 9120000000, "usage_in_usermode": 4390000000}, "system_cpu_usage": 122696628590000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 20296535800, "percpu_usage": [892538893, 420320021, 1097550713, 583595590, 1343267241, 668581360, 1582239910, 2736778789, 1047957913, 2166130402, 1484099114, 2703047750, 19266882, 33918049, 375942607, 233247927, 758069855, 34755454, 511538233, 211139202, 517712585, 133242328, 281710487, 459884495], "usage_in_kernelmode": 13600000000, "usage_in_usermode": 5940000000}, "system_cpu_usage": 122697108430000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "1024": [{"cpu_usage": {"total_usage": 14390923925, "percpu_usage": [257986801, 589744634, 882285502, 284706549, 824698152, 182287375, 1706431319, 1775165269, 1091607532, 1869034358, 2077466732, 1236189854, 16170401, 9462411, 74194378, 5421034, 1216157, 569500870, 192509450, 330412753, 146903001, 43719336, 152377520, 71432537], "usage_in_kernelmode": 9330000000, "usage_in_usermode": 4560000000}, "system_cpu_usage": 122698112280000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 22543423252, "percpu_usage": [434475408, 785418600, 1096600015, 466568005, 923848449, 237898868, 2344571695, 3016388728, 1796451869, 2982917214, 3172668616, 1807834074, 16530461, 732441907, 79665897, 5421034, 1216157, 569500870, 195541127, 354336024, 150636705, 72317640, 1085408305, 214765584], "usage_in_kernelmode": 14590000000, "usage_in_usermode": 7090000000}, "system_cpu_usage": 122698663390000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "2048": [{"cpu_usage": {"total_usage": 14727289954, "percpu_usage": [168065228, 618575835, 220995753, 19052142, 144291248, 53124958, 1376945866, 2035760964, 2182501322, 1627470177, 1976659589, 1724205434, 6883052, 4157665, 10463154, 744875175, 63976381, 12186987, 505924255, 266160389, 45556637, 9637822, 348181041, 561638880], "usage_in_kernelmode": 9600000000, "usage_in_usermode": 4710000000}, "system_cpu_usage": 122699690130000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 22828433149, "percpu_usage": [210636537, 718010058, 251955636, 71532346, 164203174, 91995206, 2328368192, 3464409208, 3192691655, 2749176686, 3303286755, 2855997747, 234999025, 4157665, 51628067, 744875175, 198663763, 55090767, 602097813, 266608088, 45556637, 39642337, 375390543, 807460069], "usage_in_kernelmode": 14970000000, "usage_in_usermode": 7280000000}, "system_cpu_usage": 122700218980000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "4096": [{"cpu_usage": {"total_usage": 12810108616, "percpu_usage": [1794903825, 2116925687, 771832116, 1465787105, 1436224196, 2045231003, 396303901, 56239256, 569366968, 241339916, 151055201, 100451346, 10310190, 127256747, 224877068, 41487193, 725793521, 129983145, 193580965, 20296408, 186034855, 2278109, 593184, 1956711], "usage_in_kernelmode": 8290000000, "usage_in_usermode": 4180000000}, "system_cpu_usage": 122701056410000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 19339003029, "percpu_usage": [2652420205, 2609991595, 1287089776, 2068207751, 2567969153, 3063931285, 662967667, 356761873, 717057862, 450407530, 233050601, 159337890, 169821888, 127256747, 415465798, 99010855, 809837179, 329793965, 193788308, 20296408, 186034855, 2278109, 154269018, 1956711], "usage_in_kernelmode": 12870000000, "usage_in_usermode": 5760000000}, "system_cpu_usage": 122701560490000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "8192": [{"cpu_usage": {"total_usage": 12754634839, "percpu_usage": [1135244852, 2255769598, 929334247, 1336828778, 1907202870, 1999367205, 71832007, 159236625, 102593021, 368212005, 129657169, 509395965, 97004861, 281871841, 311768922, 133872661, 340201687, 19091697, 0, 290415022, 5490530, 71354502, 3432111, 295456663], "usage_in_kernelmode": 8270000000, "usage_in_usermode": 4030000000}, "system_cpu_usage": 122702421330000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 18175405007, "percpu_usage": [1809418591, 2731190711, 1459812064, 2359558824, 2796097763, 3282089786, 71832007, 159236625, 102593021, 368212005, 129657169, 509395965, 298727422, 281871841, 325962910, 134025847, 521997103, 167576525, 0, 290415022, 5490530, 71354502, 3432111, 295456663], "usage_in_kernelmode": 12240000000, "usage_in_usermode": 5360000000}, "system_cpu_usage": 122702831110000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "16384": [{"cpu_usage": {"total_usage": 14277077532, "percpu_usage": [879237290, 320025937, 319640465, 419617320, 385884037, 261165242, 1087300682, 1351833157, 1347456804, 1864250236, 2441025207, 1417758206, 496677, 6878247, 4465281, 30249752, 66941681, 254465850, 327675452, 420304412, 526976161, 114688843, 428740593, 0], "usage_in_kernelmode": 9350000000, "usage_in_usermode": 4550000000}, "system_cpu_usage": 122703810430000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 20800474514, "percpu_usage": [1104138393, 421468108, 360467628, 518415511, 403430957, 435952333, 1413037362, 1579691483, 1718195361, 2917034243, 2941887143, 1699970096, 496677, 6878247, 4465281, 30249752, 66941681, 254465850, 3367961212, 448129044, 526976161, 114688843, 435283058, 30250090], "usage_in_kernelmode": 13950000000, "usage_in_usermode": 6240000000}, "system_cpu_usage": 122704291680000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "32768": [{"cpu_usage": {"total_usage": 14313472672, "percpu_usage": [1718281829, 584975388, 405256704, 949864487, 663140599, 1535825852, 787458768, 695503833, 924390264, 1284088907, 1096309642, 492688503, 1757908611, 241502675, 28747768, 37214192, 81387226, 147658736, 81414880, 39214955, 442044107, 128030995, 183373812, 7189939], "usage_in_kernelmode": 9030000000, "usage_in_usermode": 4770000000}, "system_cpu_usage": 122705224580000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 20511109066, "percpu_usage": [2173746770, 753344660, 515946747, 1237099536, 813373691, 2344342470, 1394158836, 969896907, 1321819321, 1484382895, 1347046105, 608503660, 1762361398, 241502675, 33650601, 240487942, 81387226, 315337345, 1298711832, 206322938, 536830588, 128030995, 690405958, 12417970], "usage_in_kernelmode": 13490000000, "usage_in_usermode": 6300000000}, "system_cpu_usage": 122705680950000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "65536": [{"cpu_usage": {"total_usage": 13867608537, "percpu_usage": [750552148, 320694673, 145741045, 167826268, 344003108, 310358083, 1530689559, 1307788114, 2425905839, 960205525, 1380916442, 796460372, 16400854, 366899688, 9770628, 28882834, 319604568, 169831421, 20737516, 578252628, 460484124, 1057730666, 136285516, 261586918], "usage_in_kernelmode": 9030000000, "usage_in_usermode": 4320000000}, "system_cpu_usage": 122706613170000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 20701279552, "percpu_usage": [908128477, 364211283, 205034590, 180772906, 470257168, 357760240, 2155336219, 2444986087, 3785520654, 1452347879, 2269077224, 1616864106, 16400854, 384922663, 9770628, 28882834, 319604568, 287017833, 20737516, 819128934, 461119632, 1358280952, 141289980, 643826325], "usage_in_kernelmode": 13840000000, "usage_in_usermode": 6060000000}, "system_cpu_usage": 122707117750000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "131072": [{"cpu_usage": {"total_usage": 15371989383, "percpu_usage": [2610059001, 1564022787, 1018541234, 1951644239, 1769064161, 1334323201, 595377021, 373371376, 319898100, 484061321, 316247976, 438047906, 594203777, 234895203, 364311884, 638630292, 374137274, 289734077, 22295359, 459175, 78664019, 0, 0, 0], "usage_in_kernelmode": 9800000000, "usage_in_usermode": 5000000000}, "system_cpu_usage": 122708168180000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 22978862043, "percpu_usage": [3444225079, 2637847661, 1302201902, 2827653455, 3344016249, 2598758548, 946808127, 952083759, 365326377, 561322160, 359023707, 445911256, 595352247, 325593586, 381828242, 794769421, 432748555, 290492341, 22295359, 459175, 347797323, 855189, 0, 1492325], "usage_in_kernelmode": 14820000000, "usage_in_usermode": 7450000000}, "system_cpu_usage": 122708696700000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "262144": [{"cpu_usage": {"total_usage": 15263177536, "percpu_usage": [225840252, 71854379, 97807683, 220886455, 100644049, 74367671, 2239611088, 1676045995, 1662387084, 2107963390, 1878430104, 1284901434, 355101, 527138302, 600915848, 715213491, 9210128, 0, 212796387, 282805730, 4248635, 145808591, 76638448, 1047307291], "usage_in_kernelmode": 9810000000, "usage_in_usermode": 5110000000}, "system_cpu_usage": 122709771340000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 22471151712, "percpu_usage": [575450885, 584930796, 314006095, 419403761, 150875213, 302294596, 3325841674, 2199863984, 2403107647, 2879594331, 2454066972, 1755040375, 70589383, 527138302, 885518674, 715213491, 9210128, 0, 408934084, 284332215, 4710951, 145808591, 1007912273, 1047307291], "usage_in_kernelmode": 14530000000, "usage_in_usermode": 7360000000}, "system_cpu_usage": 122710252340000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "524288": [{"cpu_usage": {"total_usage": 15441247363, "percpu_usage": [2237284397, 1578598692, 1458394477, 2519427618, 2155081532, 1894408212, 402692606, 404063826, 721428949, 288968669, 611282307, 304764184, 120220214, 227747678, 161912811, 83712796, 5690325, 91876949, 0, 25840873, 36915208, 36758568, 1695295, 72481177], "usage_in_kernelmode": 9980000000, "usage_in_usermode": 4940000000}, "system_cpu_usage": 122711326350000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 22678354638, "percpu_usage": [3139023641, 2733980118, 2274815218, 2903607819, 2846858265, 2768424555, 851341969, 519283648, 742396254, 353497431, 671634570, 684020390, 238001369, 527225056, 327861222, 123331056, 84286781, 574700744, 0, 25840873, 36915208, 37279231, 141548043, 72481177], "usage_in_kernelmode": 14840000000, "usage_in_usermode": 7240000000}, "system_cpu_usage": 122711806320000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}], "1048576": [{"cpu_usage": {"total_usage": 14697232558, "percpu_usage": [2257333968, 2196877076, 1440305360, 1149186548, 2605480444, 2813013636, 53242858, 10086222, 86138618, 13312371, 24124819, 22968923, 280173055, 58409874, 355583782, 25478270, 507440727, 316471733, 25934749, 394668521, 35483044, 21175458, 4342502, 0], "usage_in_kernelmode": 9530000000, "usage_in_usermode": 4600000000}, "system_cpu_usage": 122712857560000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}, {"cpu_usage": {"total_usage": 22171723043, "percpu_usage": [3178683352, 2573167090, 1993879603, 1809511192, 2879709726, 3742677604, 171459635, 109296721, 288837710, 44594799, 111765882, 457543194, 413444460, 58409874, 450922186, 342280441, 553765932, 1289547210, 507435317, 1063672049, 35483044, 91293520, 4342502, 0], "usage_in_kernelmode": 14430000000, "usage_in_usermode": 7030000000}, "system_cpu_usage": 122713360630000000, "online_cpus": 24, "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0}}]}
    for key in data.keys():
        old = data[key][0]['cpu_usage']['total_usage'] + data[key][0]['system_cpu_usage']
        now = data[key][1]['cpu_usage']['total_usage'] + data[key][1]['system_cpu_usage']
        print(now)
        print(old)
        res.append(now - old)
    print(json.dumps(res))

# collect()