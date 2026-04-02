from django.core.management.base import BaseCommand

from showcase.models import Breed


BREEDS = [
    {"code": 1, "name": "柴犬", "sort_order": 10},
    {"code": 2, "name": "秋田犬", "sort_order": 20},
    {"code": 3, "name": "甲斐犬", "sort_order": 30},
    {"code": 4, "name": "紀州犬", "sort_order": 40},
    {"code": 5, "name": "四国犬", "sort_order": 50},
    {"code": 6, "name": "北海道犬", "sort_order": 60},
    {"code": 7, "name": "豆柴", "sort_order": 70},
    {"code": 8, "name": "トイ・プードル", "sort_order": 80},
    {"code": 9, "name": "ミニチュア・ダックスフンド", "sort_order": 90},
    {"code": 10, "name": "チワワ", "sort_order": 100},
    {"code": 11, "name": "ポメラニアン", "sort_order": 110},
    {"code": 12, "name": "マルチーズ", "sort_order": 120},
    {"code": 13, "name": "ヨークシャー・テリア", "sort_order": 130},
    {"code": 14, "name": "シー・ズー", "sort_order": 140},
    {"code": 15, "name": "パグ", "sort_order": 150},
    {"code": 16, "name": "フレンチ・ブルドッグ", "sort_order": 160},
    {"code": 17, "name": "ミニチュア・シュナウザー", "sort_order": 170},
    {"code": 18, "name": "キャバリア", "sort_order": 180},
    {"code": 19, "name": "ビション・フリーゼ", "sort_order": 190},
    {"code": 20, "name": "ペキニーズ", "sort_order": 200},
    {"code": 21, "name": "ウェルシュ・コーギー・ペンブローク", "sort_order": 210},
    {"code": 22, "name": "シェットランド・シープドッグ", "sort_order": 220},
    {"code": 23, "name": "ボーダー・コリー", "sort_order": 230},
    {"code": 24, "name": "ラブラドール・レトリーバー", "sort_order": 240},
    {"code": 25, "name": "ゴールデン・レトリーバー", "sort_order": 250},
    {"code": 26, "name": "ジャック・ラッセル・テリア", "sort_order": 260},
    {"code": 27, "name": "ビーグル", "sort_order": 270},
    {"code": 28, "name": "ボストン・テリア", "sort_order": 280},
    {"code": 29, "name": "アメリカン・コッカー・スパニエル", "sort_order": 290},
    {"code": 30, "name": "イタリアン・グレーハウンド", "sort_order": 300},
    {"code": 31, "name": "ミニチュア・ピンシャー", "sort_order": 310},
    {"code": 32, "name": "パピヨン", "sort_order": 320},
    {"code": 33, "name": "サモエド", "sort_order": 330},
    {"code": 34, "name": "シベリアン・ハスキー", "sort_order": 340},
    {"code": 35, "name": "バーニーズ・マウンテン・ドッグ", "sort_order": 350},
    {"code": 36, "name": "ドーベルマン", "sort_order": 360},
    {"code": 37, "name": "グレート・ピレニーズ", "sort_order": 370},
    {"code": 38, "name": "ダルメシアン", "sort_order": 380},
    {"code": 39, "name": "ウィペット", "sort_order": 390},
    {"code": 40, "name": "ボルゾイ", "sort_order": 400},
]


class Command(BaseCommand):
    help = "showcase_breed に主要犬種マスタを投入/更新する"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for item in BREEDS:
            defaults = {
                "name": item["name"],
                "sort_order": item["sort_order"],
            }
            _, created = Breed.objects.update_or_create(code=item["code"], defaults=defaults)
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"seed_breeds completed: created={created_count}, updated={updated_count}, total={len(BREEDS)}"
            )
        )
