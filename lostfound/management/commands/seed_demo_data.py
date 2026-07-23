from datetime import date
from pathlib import Path
import re

from django.core.management.base import BaseCommand

from lostfound.models import ClaimRequest, Item


SUBMITTERS = [
    ('Jordan Lee', 'jordan.lee@school.edu', '555-0101'),
    ('Avery Patel', 'avery.patel@school.edu', '555-0102'),
    ('Morgan Diaz', 'morgan.diaz@school.edu', '555-0103'),
    ('Taylor Green', 'taylor.green@school.edu', '555-0104'),
    ('Casey Nguyen', 'casey.nguyen@school.edu', '555-0105'),
    ('Riley Thompson', 'riley.thompson@school.edu', '555-0106'),
    ('Dakota Brown', 'dakota.brown@school.edu', '555-0107'),
    ('Alex Rivera', 'alex.rivera@school.edu', '555-0108'),
]


SEED_ITEMS = [
    {
        'filename': 'Airpods.jpg',
        'location_found': 'Library study room 4',
        'date_found': date(2025, 12, 3),
        'status': 'pending',
    },
    {
        'filename': 'Black Airpods.jpg',
        'location_found': 'Media lab desk',
        'date_found': date(2025, 12, 6),
        'status': 'approved',
    },
    {
        'filename': 'Black FBLA Backpack.jpg',
        'location_found': 'Student center lockers',
        'date_found': date(2025, 12, 9),
        'status': 'approved',
    },
    {
        'filename': 'Black Hoodie.jpg',
        'location_found': 'Auditorium seat row F',
        'date_found': date(2025, 12, 12),
        'status': 'approved',
    },
    {
        'filename': 'Black Jacket.jpg',
        'location_found': 'Front office coat rack',
        'date_found': date(2025, 12, 15),
        'status': 'approved',
    },
    {
        'filename': 'Black Lunchbox.jpg',
        'location_found': 'Cafeteria table 3',
        'date_found': date(2025, 12, 18),
        'status': 'approved',
    },
    {
        'filename': 'Black Macbook Air.jpg',
        'location_found': 'Library tech desk',
        'date_found': date(2025, 12, 21),
        'status': 'approved',
    },
    {
        'filename': 'Black Notebook.jpg',
        'location_found': 'Math hallway bench',
        'date_found': date(2025, 12, 24),
        'status': 'approved',
    },
    {
        'filename': 'Black Swiss Backpack.jpg',
        'location_found': 'Locker bay C',
        'date_found': date(2025, 12, 27),
        'status': 'approved',
    },
    {
        'filename': 'Black Wallet.jpg',
        'location_found': 'Cafeteria checkout line',
        'date_found': date(2025, 12, 30),
        'status': 'pending',
    },
    {
        'filename': 'Black_Nike_Hoodie.jpg',
        'location_found': 'Gym bleachers',
        'date_found': date(2026, 1, 2),
        'status': 'approved',
    },
    {
        'filename': 'Blue Accordian Folder.jpg',
        'location_found': 'English classroom 12',
        'date_found': date(2026, 1, 5),
        'status': 'approved',
    },
    {
        'filename': 'Blue Backpack.jpg',
        'location_found': 'Bus loop bench',
        'date_found': date(2026, 1, 8),
        'status': 'approved',
    },
    {
        'filename': 'Blue Diary.jpg',
        'location_found': 'Front office lost shelf',
        'date_found': date(2026, 1, 11),
        'status': 'approved',
    },
    {
        'filename': 'Blue Notebook.jpg',
        'location_found': 'Science wing table',
        'date_found': date(2026, 1, 14),
        'status': 'approved',
    },
    {
        'filename': 'Blue_Hydroflask_Bottle.jpg',
        'location_found': 'Gym bleachers',
        'date_found': date(2026, 1, 17),
        'status': 'approved',
    },
    {
        'filename': 'Camo Lunchbox.jpg',
        'location_found': 'Student union tables',
        'date_found': date(2026, 1, 20),
        'status': 'approved',
    },
    {
        'filename': 'Car Keys.jpg',
        'location_found': 'Main lobby sofa',
        'date_found': date(2026, 1, 23),
        'status': 'approved',
    },
    {
        'filename': 'Clear Black Watterbottle.jpg',
        'location_found': 'Locker room bench',
        'date_found': date(2026, 1, 26),
        'status': 'approved',
    },
    {
        'filename': 'Computer Charger.jpg',
        'location_found': 'Media lab charging cart',
        'date_found': date(2026, 1, 29),
        'status': 'pending',
    },
    {
        'filename': 'Glasses.jpg',
        'location_found': 'Library reading nook',
        'date_found': date(2026, 2, 1),
        'status': 'approved',
    },
    {
        'filename': 'Graphing_Calculator.jpg',
        'location_found': 'Math classroom 204',
        'date_found': date(2026, 2, 4),
        'status': 'approved',
    },
    {
        'filename': 'Green Notebook.jpg',
        'location_found': 'Art room desk',
        'date_found': date(2026, 2, 7),
        'status': 'approved',
    },
    {
        'filename': 'Grey Backpack.jpg',
        'location_found': 'Hallway outside guidance',
        'date_found': date(2026, 2, 10),
        'status': 'approved',
    },
    {
        'filename': 'Grey Hp Computer.jpg',
        'location_found': 'IT office counter',
        'date_found': date(2026, 2, 13),
        'status': 'approved',
    },
    {
        'filename': 'Grey Wallet.jpg',
        'location_found': 'Auditorium row H',
        'date_found': date(2026, 2, 16),
        'status': 'approved',
    },
    {
        'filename': 'Jarritos Drink.jpg',
        'location_found': 'Cafeteria lunch table',
        'date_found': date(2026, 2, 19),
        'status': 'approved',
    },
    {
        'filename': 'Light Blue Watterbottle.jpg',
        'location_found': 'Tennis court bench',
        'date_found': date(2026, 2, 22),
        'status': 'pending',
    },
    {
        'filename': 'Orange Lunchbox.jpg',
        'location_found': 'Bus loop bench',
        'date_found': date(2026, 2, 25),
        'status': 'approved',
    },
    {
        'filename': 'Orange Notebook.jpg',
        'location_found': 'English hallway shelf',
        'date_found': date(2026, 2, 28),
        'status': 'approved',
    },
    {
        'filename': 'Parli Book.jpg',
        'location_found': 'Library return cart',
        'date_found': date(2026, 3, 2),
        'status': 'approved',
    },
    {
        'filename': 'Phone Cracked Screen.jpg',
        'location_found': 'Courtyard bench',
        'date_found': date(2026, 3, 5),
        'status': 'pending',
    },
    {
        'filename': 'Poisonwood Book.jpg',
        'location_found': 'Social studies room shelf',
        'date_found': date(2026, 3, 8),
        'status': 'approved',
    },
    {
        'filename': 'Powerbank.jpg',
        'location_found': 'Science lab cart',
        'date_found': date(2026, 3, 11),
        'status': 'approved',
    },
    {
        'filename': 'Psych Textbook.jpg',
        'location_found': 'Counseling office waiting area',
        'date_found': date(2026, 3, 14),
        'status': 'approved',
    },
    {
        'filename': 'Red Backpack.jpg',
        'location_found': 'Locker bay A',
        'date_found': date(2026, 3, 17),
        'status': 'approved',
    },
    {
        'filename': 'School Computer.jpg',
        'location_found': 'Computer cart in room 305',
        'date_found': date(2026, 3, 20),
        'status': 'approved',
    },
    {
        'filename': 'Scissors.jpg',
        'location_found': 'Art room supply shelf',
        'date_found': date(2026, 3, 23),
        'status': 'approved',
    },
    {
        'filename': 'Stats Textbook.jpg',
        'location_found': 'Math department shelf',
        'date_found': date(2026, 3, 26),
        'status': 'approved',
    },
    {
        'filename': 'TI-84 Plus Graphic Calc.jpg',
        'location_found': 'Math classroom 204',
        'date_found': date(2026, 3, 29),
        'status': 'approved',
    },
    {
        'filename': 'Yellow Notebook.jpg',
        'location_found': 'Student center table',
        'date_found': date(2026, 3, 31),
        'status': 'approved',
    },
]


CLAIM_REQUESTS = [
    {
        'item_index': 6,
        'claimant_name': 'Riley Thompson',
        'claimant_email': 'riley.thompson@student.school.edu',
        'claimant_phone': '555-1010',
        'proof_of_ownership': 'Serial number and case scratches match my laptop.',
        'additional_message': 'I lost it after computer lab on Tuesday.',
        'status': 'pending',
    },
    {
        'item_index': 15,
        'claimant_name': 'Dakota Brown',
        'claimant_email': 'dakota.brown@student.school.edu',
        'claimant_phone': '555-2020',
        'proof_of_ownership': 'Bottle has my initials on the base sticker.',
        'additional_message': 'Can pick it up before practice.',
        'status': 'reviewed',
    },
]


def normalize_title(filename):
    stem = Path(filename).stem.replace('_', ' ')
    stem = re.sub(r'\s+', ' ', stem).strip()
    title = stem.title()
    replacements = {
        'Airpods': 'AirPods',
        'Fbla': 'FBLA',
        'Hp': 'HP',
        'Macbook': 'MacBook',
        'Hydroflask': 'Hydro Flask',
        'Watterbottle': 'Water Bottle',
        'Accordian': 'Accordion',
        'Ti-84 Plus Graphic Calc': 'TI-84 Plus Graphing Calculator',
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title


def infer_category(filename):
    stem = filename.lower()
    if any(keyword in stem for keyword in ('hoodie', 'jacket')):
        return 'clothing'
    if any(keyword in stem for keyword in ('airpods', 'phone', 'computer', 'charger', 'powerbank')):
        return 'electronics'
    if any(keyword in stem for keyword in ('wallet', 'glasses', 'keys', 'bottle', 'drink')):
        return 'accessories'
    if any(keyword in stem for keyword in ('calculator', 'notebook', 'diary', 'folder', 'book', 'textbook', 'backpack', 'lunchbox', 'scissors')):
        return 'school'
    return 'other'


def build_description(filename, title):
    stem = filename.lower()
    if 'airpods' in stem:
        return f'{title} wireless earbuds in a compact charging case.'
    if 'backpack' in stem:
        return f'{title} with multiple zippered compartments and no visible name tag.'
    if 'hoodie' in stem:
        return f'{title} with no visible name tag.'
    if 'jacket' in stem:
        return f'{title} folded neatly when it was turned in.'
    if 'lunchbox' in stem:
        return f'{title} with a hard shell and insulated lining.'
    if 'macbook air' in stem or 'computer' in stem:
        return f'{title} laptop with a clean outer shell and no visible owner label.'
    if 'notebook' in stem:
        return f'{title} spiral notebook with handwritten class notes inside.'
    if 'diary' in stem:
        return f'{title} planner with personal notes and reminders.'
    if 'wallet' in stem:
        return f'{title} with card slots and no loose cash visible.'
    if 'folder' in stem:
        return f'{title} folder holding loose class papers.'
    if 'hydroflask' in stem or 'watterbottle' in stem or 'bottle' in stem:
        return f'{title} reusable bottle with a screw-top lid.'
    if 'keys' in stem:
        return f'{title} on a simple key ring.'
    if 'charger' in stem:
        return f'{title} with the cable wrapped for storage.'
    if 'glasses' in stem:
        return f'{title} with a dark frame and clear lenses.'
    if 'calculator' in stem or 'calc' in stem:
        return f'{title} graphing calculator with visible keypad buttons.'
    if 'book' in stem or 'textbook' in stem:
        return f'{title} with worn edges and classroom notes inside.'
    if 'phone' in stem:
        return f'{title} with a cracked screen and no visible case design.'
    if 'powerbank' in stem:
        return f'{title} portable charger with USB ports.'
    if 'scissors' in stem:
        return f'{title} pair of school scissors with colored handles.'
    if 'drink' in stem:
        return f'{title} beverage bottle left behind after lunch.'
    return f'{title} found and turned in to staff with no visible name label.'


class Command(BaseCommand):
    help = 'Create sample lost-and-found records for demos and judging presentations.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing Item and ClaimRequest data before seeding.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            ClaimRequest.objects.all().delete()
            Item.objects.all().delete()
            self.stdout.write(self.style.WARNING('Existing data cleared.'))

        if Item.objects.exists() and not options['reset']:
            self.stdout.write(
                self.style.WARNING(
                    'Data already exists. Use --reset to recreate fresh demo records.'
                )
            )
            return

        created_items = []
        for index, seed_item in enumerate(SEED_ITEMS):
            title = normalize_title(seed_item['filename'])
            category = infer_category(seed_item['filename'])
            submitted_by_name, submitted_by_email, submitted_by_phone = SUBMITTERS[index % len(SUBMITTERS)]
            created_items.append(
                Item.objects.create(
                    title=title,
                    category=category,
                    description=build_description(seed_item['filename'], title),
                    location_found=seed_item['location_found'],
                    date_found=seed_item['date_found'],
                    image=f"item_photos/{seed_item['filename']}",
                    submitted_by_name=submitted_by_name,
                    submitted_by_email=submitted_by_email,
                    submitted_by_phone=submitted_by_phone,
                    status=seed_item['status'],
                )
            )

        for claim_seed in CLAIM_REQUESTS:
            ClaimRequest.objects.create(
                item=created_items[claim_seed['item_index']],
                claimant_name=claim_seed['claimant_name'],
                claimant_email=claim_seed['claimant_email'],
                claimant_phone=claim_seed['claimant_phone'],
                proof_of_ownership=claim_seed['proof_of_ownership'],
                additional_message=claim_seed['additional_message'],
                status=claim_seed['status'],
            )

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
        self.stdout.write(
            self.style.SUCCESS(
                f'Created {len(created_items)} items and {ClaimRequest.objects.count()} claim records.'
            )
        )
