from api import get_all_videos
from did import get_did

user_list = {
    '3x2fjihh75iaz2m': "星韩汐",
    '3xhddn5sus9m4f9': "🍹·祎杯颖料·🍹",
    '3xy3uwf6bn5bmeq': "色.橘.恋.祎.记",
    '3xksx86nx6mjvms': ".汐月带鞠私奔.",
}

if __name__ == '__main__':
    did = get_did()
    print("did:",did)
    for kid,name in user_list.items():
        print(get_all_videos(kid,name,did))
