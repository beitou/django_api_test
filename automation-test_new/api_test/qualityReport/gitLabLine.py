import logging

from requests import RequestException
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from xpinyin import Pinyin
from api_test.common.api_response import JsonResponse
from api_test.common.gitlab_api import GitLabApi
from api_test.common.name_mapping import get_git_name

logger = logging.getLogger(__name__) # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class GitLabLine(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        startTime = request.GET.get("startTime")
        endTime = request.GET.get("endTime")
        # p = Pinyin()
        # g = GitLabApi(0, startTime, endTime)
        # userSubmit = g.getAllLins()
        # projectId = g.getAllProjectLins()
        # projectId = [1229, 1228, 1226, 1225, 1224, 1223, 1222, 1221, 1220, 1219, 1218, 1217, 1216, 1215, 1214, 1212, 1211, 1209, 1207, 1206, 1204, 1203, 1202, 1201, 1200, 1199, 1198, 1197, 1196, 1195, 1194, 1193, 1192, 1191, 1190, 1188, 1187, 1186, 1184, 1183, 1182, 1181, 1180, 1179, 1178, 1177, 1176, 1174, 1173, 1172, 1171, 1170, 1168, 1167, 1166, 1165, 1164, 1163, 1162, 1161, 1160, 1159, 1157, 1156, 1155, 1154, 1152, 1151, 1150, 1149, 1148, 1147, 1146, 1145, 1144, 1143, 1142, 1141, 1140, 1139, 1138, 1137, 1136, 1134, 1132, 1131, 1130, 1129, 1128, 1127, 1126, 1125, 1124, 1123, 1122, 1121, 1120, 1119, 1118, 1117, 1114, 1113, 1112, 1111, 1110, 1109, 1108, 1105, 1104, 1103, 1102, 1101, 1099, 1098, 1097, 1096, 1095, 1093, 1092, 1091, 1090, 1089, 1088, 1087, 1086, 1085, 1084, 1083, 1082, 1081, 1080, 1079, 1078, 1077, 1076, 1075, 1074, 1073, 1069, 1068, 1067, 1065, 1064, 1063, 1062, 1058, 1057, 1056, 1055, 1053, 1052, 1049, 1048, 1047, 1046, 1045, 1043, 1042, 1041, 1040, 1039, 1038, 1037, 1036, 1035, 1034, 1033, 1030, 1029, 1028, 1027, 1025, 1024, 1023, 1022, 1021, 1020, 1019, 1018, 1017, 1016, 1014, 1010, 1007, 1006, 1005, 1004, 1003, 1001, 995, 993, 991, 990, 988, 982, 981, 979, 978, 977, 976, 973, 972, 971, 963, 962, 961, 960, 959, 958, 954, 953, 952, 951, 945, 943, 942, 939, 936, 934, 933, 932, 929, 928, 927, 926, 924, 923, 922, 921, 920, 919, 918, 917, 916, 915, 911, 910, 909, 908, 907, 906, 905, 904, 903, 900, 897, 894, 893, 892, 891, 890, 889, 888, 887, 886, 885, 884, 879, 877, 874, 873, 872, 871, 870, 869, 868, 866, 865, 862, 861, 860, 859, 858, 856, 855, 854, 853, 850, 848, 847, 846, 845, 842, 839, 838, 837, 836, 835, 830, 828, 827, 824, 822, 820, 816, 815, 814, 813, 806, 805, 804, 803, 800, 798, 797, 796, 792, 787, 786, 785, 783, 782, 779, 778, 777, 774, 773, 771, 770, 769, 768, 767, 766, 765, 763, 762, 761, 760, 759, 757, 756, 754, 753, 752, 750, 749, 748, 747, 745, 744, 743, 740, 738, 737, 736, 735, 734, 733, 732, 731, 730, 728, 723, 722, 720, 719, 717, 713, 712, 706, 703, 702, 701, 700, 698, 696, 692, 689, 685, 684, 682, 681, 678, 672, 671, 669, 668, 667, 665, 664, 662, 661, 659, 657, 656, 655, 653, 652, 651, 649, 647, 646, 645, 643, 642, 641, 639, 638, 637, 636, 634, 633, 631, 630, 629, 626, 625, 624, 621, 620, 617, 614, 613, 612, 611, 610, 608, 606, 603, 602, 601, 600, 598, 597, 596, 594, 593, 591, 590, 589, 588, 587, 586, 585, 584, 583, 582, 581, 580, 579, 578, 577, 576, 575, 574, 572, 571, 570, 568, 563, 562, 561, 560, 559, 558, 557, 556, 555, 554, 553, 552, 550, 549, 548, 547, 546, 545, 544, 543, 542, 540, 537, 535, 534, 532, 530, 529, 528, 527, 525, 524, 523, 522, 520, 519, 518, 517, 516, 515, 514, 513, 512, 508, 506, 505, 501, 500, 499, 496, 495, 493, 491, 489, 488, 487, 486, 485, 484, 482, 481, 480, 479, 478, 477, 476, 475, 474, 473, 472, 471, 470, 469, 468, 467, 466, 465, 463, 462, 461, 460, 459, 458, 457, 456, 455, 454, 453, 452, 451, 449, 448, 447, 446, 445, 442, 441, 440, 438, 437, 436, 435, 434, 433, 432, 431, 430, 429, 428, 427, 426, 425, 424, 423, 422, 421, 420, 419, 418, 417, 416, 415, 414, 413, 412, 409, 408, 407, 406, 405, 404, 402, 401, 400, 399, 398, 397, 396, 395, 394, 393, 392, 391, 390, 386, 385, 384, 383, 381, 380, 379, 378, 377, 375, 374, 373, 372, 371, 370, 369, 368, 367, 366, 365, 364, 363, 362, 361, 360, 359, 357, 352, 350, 349, 348, 347, 346, 344, 342, 340, 337, 336, 335, 334, 331, 330, 329, 327, 326, 325, 323, 322, 319, 318, 317, 314, 313, 312, 311, 310, 309, 307, 306, 305, 303, 302, 301, 300, 298, 297, 295, 294, 293, 292, 291, 290, 289, 288, 287, 286, 285, 284, 283, 282, 280, 279, 278, 277, 276, 275, 273, 272, 271, 269, 264, 262, 260, 257, 255, 253, 252, 251, 250, 248, 247, 246, 245, 244, 243, 242, 241, 239, 238, 237, 236, 235, 234, 233, 232, 230, 229, 228, 227, 226, 225, 224, 223, 222, 221, 220, 219, 218, 217, 216, 215, 214, 211, 210, 209, 207, 206, 204, 203, 202, 201, 200, 199, 198, 197, 195, 193, 192, 191, 190, 188, 187, 185, 181, 180, 178, 176, 172, 167, 165, 163, 162, 159, 157, 155, 154, 153, 152, 151, 148, 145, 142, 141, 140, 138, 137, 134, 132, 131, 123, 122, 118, 114, 113, 111, 108, 101, 97, 95, 92, 90, 84, 83, 79, 77, 76, 69, 67, 64, 63, 62, 58, 57, 55, 54, 52, 50, 49, 47, 45, 38, 36, 35, 29, 28, 27, 26, 25, 24, 23, 22, 19, 15, 13, 8, 7, 5, 4, 1]
        userSubmit = {}
        try:
            # for id in projectId:
            #     g = GitLabApi(id, startTime, endTime)
            #     commits = g.getAllCommits()
            #     for commit in commits:
            #         for ch in commit['author_name']:
            #             # 中文转英文
            #             if u'\u4e00' <= ch <= u'\u9fff':
            #                 commit['author_name'] = p.get_pinyin(commit['author_name'], '')
            #                 break
            #         commit['author_name'] = get_git_name(commit['author_name'])
            #         # 统计
            #         if commit['author_name'] in userSubmit.keys():
            #             userSubmit[commit['author_name']] += commit['total']
            #         else:
            #             userSubmit.update({commit['author_name']: commit['total']})
            g = GitLabApi(0, startTime, endTime)
            userSubmit = g.getAllLins()
            user_submit_sort = dict(sorted(userSubmit.items(), key=lambda submit: submit[1], reverse=False))
            submit_total = 0
            for key in userSubmit:
                submit_total += userSubmit.get(key)
        except RequestException:
            return JsonResponse(code="999998", msg="蝉道请求失败!")
        return JsonResponse(data={"userSubmit": user_submit_sort, 'submit_total': submit_total}, code="999999", msg="成功")
