import pygame
import random
import sys
from time import sleep as wait

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
game_name: str = "UltraBeing"
pygame.display.set_caption(f"{game_name}")
pygame.display.set_icon(pygame.image.load("icon.png"))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
LIGHT_BLUE = (173, 216, 230)
GRAY = (128, 128, 128)

# Fonts
pygame.font.init()
header_font = pygame.font.SysFont('comicsansms', int(24 * WIDTH / 800), bold=True)
body_font = pygame.font.SysFont('comicsansms', int(18 * WIDTH / 1000))
stat_font = pygame.font.SysFont('comicsansms', int(18 * WIDTH / 1000))
cartoon_font = pygame.font.SysFont('comicsansms', int(20 * WIDTH / 800))

# Utility functions
def draw_text(surface, text, font, color, rect):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, rect)

def draw_button(surface, text, font, color, rect):
    pygame.draw.rect(surface, color, rect)
    draw_text(surface, text, font, WHITE, rect.move(10, 5))

def draw_progress_bar(surface, x, y, screen_width, screen_height, percentage, border_color):
    # Calculate the width and height of the progress bar based on the screen size
    bar_width = int(screen_width * 0.18)  # Adjusted to 18% of the screen width for better fit
    bar_height = int(screen_height * 0.02)  # 2% of the screen height

    # Determine the fill color based on the percentage
    if percentage >= 70:
        fill_color = GREEN
    elif percentage >= 50:
        fill_color = ORANGE
    elif percentage > 30:
        fill_color = YELLOW
    else:
        fill_color = RED
    
    # Draw the border
    pygame.draw.rect(surface, border_color, (x, y, bar_width, bar_height), 2)
    
    # Draw the filled portion of the bar
    inner_width = int(bar_width * (percentage / 100))
    pygame.draw.rect(surface, LIGHT_BLUE, (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, fill_color, (x, y, inner_width, bar_height))

last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

class Job:
    def __init__(self, name, rank, progress, reputation, coworkers, supervisor, ranks, income):
        self.name = name
        self.rank = rank
        self.progress = progress
        self.reputation = reputation
        self.coworkers = coworkers
        self.supervisor = supervisor
        self.ranks = ranks
        self.income = income
    
    def pay(self, player):
        player.money += random.randint(self.income // 2, self.income)
    
    def work(self, amount="random"):
        if self.progress < 100:
            if amount == "random":
                self.progress += random.randint(5, 20)
            elif isinstance(amount, int):
                self.progress += amount
            else:
                add_message(player, "Invalid amount!")
            if self.progress > 100:
                self.progress = 100
    
    def promote(self, amount=1):
        ranks = list(self.ranks.keys())
        rank_index = ranks.index(self.rank) + amount
        if 0 <= rank_index < len(ranks):
            self.rank = ranks[rank_index]
            self.income = self.ranks[self.rank]
            self.add_reputation()
    
    def demote(self, amount=1):
        ranks = list(self.ranks.keys())
        rank_index = ranks.index(self.rank) - amount
        if 0 <= rank_index < len(ranks):
            self.rank = ranks[rank_index]
            self.income = self.ranks[self.rank]
            self.lose_reputation()
    
    def add_reputation(self, amount="random"):
        if self.reputation < 100:
            if amount == "random":
                self.reputation += random.randint(5, 20)
            elif isinstance(amount, int):
                self.reputation += amount
            else:
                add_message(player, "Invalid amount!")
            if self.reputation > 100:
                self.reputation = 100
                
    def lose_reputation(self, amount="random"):
        if self.reputation > 0:
            if amount == "random":
                self.reputation -= random.randint(5, 20)
            elif isinstance(amount, int):
                self.reputation -= amount
            else:
                add_message(player, "Invalid amount!")
            if self.reputation < 0:
                self.reputation = 0

class Activity:
    def __init__(self, name, level, skill_boost):
        self.name = name
        self.level = level
        self.skill_boost = skill_boost
    
    def skill_up(self, skill):
        if skill.level < 5:
            skill.level += self.skill_boost
            if skill.level > 5:
                skill.level = 5

def generate_random_name(name_type, last_name=None):
    global last_names
    if name_type == "male":
        first_names = [
            "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
            "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
            "Kenneth", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
            "Jacob", "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin", "Scott", "Brandon",
            "Frank", "Benjamin", "Gregory", "Raymond", "Samuel", "Patrick", "Alexander", "Jack", "Dennis", "Jerry"
        ]
    elif name_type == "female":
        first_names = [
            "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
            "Nancy", "Margaret", "Lisa", "Betty", "Dorothy", "Sandra", "Ashley", "Kimberly", "Donna", "Emily",
            "Michelle", "Carol", "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia",
            "Kathleen", "Amy", "Shirley", "Angela", "Helen", "Anna", "Brenda", "Pamela", "Nicole", "Emma", "Samantha",
            "Katherine", "Christine", "Debra", "Rachel", "Catherine", "Carolyn", "Janet", "Maria", "Heather", "Diane"
        ]
    if name_type in ["male", "female"]:
        if last_name is None:
            last_name = random.choice(last_names)
        
        return random.choice(first_names) + " " + last_name

# Game classes
class Character:
    def __init__(self, npc=False):
        global last_names, jobs
        random_gender = random.choice(["male", "female"])
        self.first_name = generate_random_name(random_gender, None).split()[0]
        self.last_name = generate_random_name(random_gender, None).split()[0]
        self.lifespan = random.randint(80, 200)
        self.health = random.randint(20, 80)
        self.happiness = random.randint(20, 80)
        self.smarts = random.randint(20, 80)
        self.looks = random.randint(20, 80)
        self.craziness = random.randint(20, 80)
        self.willpower = random.randint(20, 80)
        self.sexuality = random.choice(["Straight", "Gay", "Bisexual"])
        self.gender = random_gender.capitalize()
        self.petulance = random.randint(20, 100)
        self.generosity = random.randint(20, 100)
        self.karma = random.randint(20, 100)
        self.job = None
        self.family = {}
        self.mother = None
        self.father = None
        self.is_jr = False
        self.is_sr = False
        month = random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        day = random.randint(1, 31)
        year = random.choice(["2018", "2019", "2020", "2021", "2022", "2023", "2024"])
        self.birthday = f"{month}, {day}, {year}"
        if npc == False:
            self.age = -1
            self.messages = []
            self.money = 0
            self.education = None
            self.assets = {"cars": {}, "houses": {}}
        else:
            self.age = 0
            self.relationship_with_player = None
            self.money = random.randint(100, 2000)
            self.education = None
            self.assets = {"cars": {}, "houses": {}}
            self.player_closeness = random.randint(30, 50)
            self.player_romance = 0
        self.relationships = {}
        self.hobbies = {}
        self.school = {
            "type": "Kindergarten",
            "grade": 0,
            "teachers": {},
            "classmates": {},
            "nurse_visits": 0,
            "activities": {
                "Art": Activity("Art", 1, 0.5),
                "Music": Activity("Music", 1, 0.5),
                "Sports": Activity("Sports", 1, 0.5),
                "Drama": Activity("Drama", 1, 0.5)
            },
            "taken_activities": {}
        }

    def randomize_stats(self, npc=False):
        global last_names, jobs
        random_gender = random.choice(["male", "female"])
        self.first_name = generate_random_name(random_gender, None).split()[0]
        self.last_name = generate_random_name(random_gender, None).split()[0]
        self.lifespan = random.randint(0, 200)
        self.health = random.randint(20, 80)
        self.happiness = random.randint(20, 80)
        self.smarts = random.randint(20, 80)
        self.looks = random.randint(20, 80)
        self.craziness = random.randint(20, 80)
        self.willpower = random.randint(20, 80)
        self.sexuality = random.choice(["Straight", "Gay", "Bisexual"])
        self.gender = random_gender.capitalize()
        self.petulance = random.randint(20, 100)
        self.generosity = random.randint(20, 100)
        self.karma = random.randint(20, 100)
        self.job = None
        self.family = {}
        self.mother = None
        self.father = None
        self.is_jr = False
        self.is_sr = False
        month = random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        day = random.randint(1, 31)
        year = random.choice(["2018", "2019", "2020", "2021", "2022", "2023", "2024"])
        self.birthday = f"{month}, {day}, {year}"
        if npc == False:
            self.age = -1
            self.messages = []
            self.money = 0
            self.education = None
            self.assets = {"cars": {}, "houses": {}}
        else:
            self.age = 0
            self.relationship_with_player = None
            self.money = random.randint(100, 2000)
            self.education = None
            self.assets = {"cars": {}, "houses": {}}
            self.player_closeness = random.randint(30, 50)
            self.player_romance = 0
        self.relationships = {}
        self.hobbies = {}
        self.school = {
            "type": "Kindergarten",
            "grade": 0,
            "teachers": {},
            "classmates": {},
            "nurse_visits": 0,
            "activities": {
                "Art": Activity("Art", 1, 0.5),
                "Music": Activity("Music", 1, 0.5),
                "Sports": Activity("Sports", 1, 0.5),
                "Drama": Activity("Drama", 1, 0.5)
            },
            "taken_activities": {}
        }

    def age_up(self):
        self.age += 1
        add_message(self, f"[event_BLUE] Age {self.age}: ", "age")
        if self.health <= 0:
            self.death()
        elif self.age >= self.lifespan:
            self.death("I died of old age!")
        else:
            if self.age == 1:
                add_message(self, "I started crawling.")
            elif self.age == 3:
                add_message(self, "I started walking.")
            elif self.age == 5:
                add_message(self, "I started talking.")
            elif self.age == 16:
                add_message(self, "I can get a driver's license!")
            if self.age != 0:
                add_message(self, random_event(self))
            else:
                if self.family[self.father].is_sr:
                    father_name = f"{self.father} Sr."
                else:
                    father_name = self.father
                if self.family[self.mother].is_sr:
                    mother_name = f"{self.mother} Sr."
                else:
                    mother_name = self.mother
                add_message(self, f"I am {self.first_name} {self.last_name}, a {self.gender}, I was born to {mother_name} and {father_name} on {self.birthday}!")
    
    def generate_family(self, family_type="npc"):
        if family_type == "player":
            last_name = self.last_name
        else:
            last_name = None
        female_name = generate_random_name("female", last_name).split(" ")
        male_name = generate_random_name("male", last_name).split(" ")
        mom = Character(True)
        mom.first_name = female_name[0]
        mom.last_name = female_name[1]
        mom.gender = "Female"
        dad = Character(True)
        dad.first_name = male_name[0]
        dad.last_name = male_name[1]
        dad.gender = "Male"
        self.add_family_member(mom, "Mother")
        self.add_family_member(dad, "Father")
        
        if random.choice([True, False]):
            num_siblings = random.randint(1, 3)
            for _ in range(num_siblings):
                sib_gender = random.choice(["female", "male"])
                sibling_name = generate_random_name(sib_gender, last_name).split(" ")
                sibling = Character(True)
                sibling.first_name = sibling_name[0]
                sibling.last_name = sibling_name[1]
                sibling.gender = sib_gender.capitalize()
                if sibling.first_name == self.father.split(" ")[0]:
                    sibling.is_jr = True
                    self.family[self.father].is_sr = True
                elif sibling.first_name == self.mother.split(" ")[0]:
                    sibling.is_jr = True
                    self.family[self.mother].is_sr = True
                if sibling.gender == "Male":
                    sib_type = "Older Brother"
                else:
                    sib_type = "Older Sister"
                self.add_family_member(sibling, f"{sib_type}")

    def add_family_member(self, member, relationship):
        if relationship == "Mother":
            self.mother = f"{member.first_name} {member.last_name}"
        elif relationship == "Father":
            self.father = f"{member.first_name} {member.last_name}"
        member.relationship_with_player = relationship
        self.family.update({f"{member.first_name} {member.last_name}": member})

    def add_relationship(self, person, relationship="Friend"):
        person.relationship_with_player = relationship
        self.relationships.update({f"{person.first_name} {person.last_name}": person})

    def interact_with_relationship(self, person, interaction_type):
        flirt_types = {
            "called": ["cute", "sexy", "beautiful", "baby"],
            "said to": ["that they are my one", "that they are my whole heart", "that I love them"]
        }
        if f"{person.first_name} {person.last_name}" in self.family:
            if person.relationship_with_player in ["Mother", "Father", "Older Brother", "Older Sister", "Younger Brother", "Younger Sister", "Twin Brother"]:
                person_called = f"my {person.relationship_with_player.lower()}, {person.first_name}"
        if interaction_type == "Spend Time":
            interaction_effect = random.randint(5, 20)
            add_message(self, f"I spent time with {person_called}. Closeness increased by {interaction_effect}.")
            person.player_closeness = min(person.player_closeness + interaction_effect, 100)
        elif interaction_type == "Argue":
            interaction_effect = random.randint(-20, -5)
            romance_effect = random.randint(-20, -5)
            if person.relationship_with_player not in ["Mother", "Father"] and person.player_romance > 1:
                add_message(self, f"I argued with {person_called}. Closeness decreased by {-interaction_effect}, and Romance decreased by {-romance_effect}.")
                person.player_romance = max(person.player_romance + interaction_effect, 0)
            else:
                add_message(self, f"I argued with {person_called}. Closeness decreased by {-interaction_effect}.")
            person.player_closeness = max(person.player_closeness + interaction_effect, 0)
        elif interaction_type == "Fight":
            interaction_effect = random.randint(-20, -5)
            romance_effect = random.randint(-20, -5)
            player_health_effect = random.randint(-20, -5)
            npc_health_effect = random.randint(-20, -5)
            if person.relationship_with_player not in ["Mother", "Father"] and person.player_romance > 1:
                add_message(self, f"I fought with {person_called}. Closeness decreased by {-interaction_effect}, and Romance decreased by {-romance_effect}.")
                person.player_romance = max(person.player_romance + interaction_effect, 0)
            else:
                add_message(self, f"I fought with {person_called}. Closeness decreased by {-interaction_effect}.")
            person.player_closeness = max(person.player_closeness + interaction_effect, 0)
            person.health = max(player.strength + npc_health_effect, 0)
            player.health = max(person.strength + player_health_effect, 0)
            if person.health <= 0:
                person.health = 0
                add_message(self, f"I killed {person_called} during a fight!")
            if player.health <= 0:
                player.health = 0
                player.death(f"I died during a fight with {person_called}.")
        elif interaction_type == "Give Gift":
            interaction_effect = random.randint(10, 30)
            add_message(self, f"I gave a gift to {person_called}. Closeness increased by {interaction_effect}.")
            person.player_closeness = min(person.player_closeness + interaction_effect, 100)
        elif interaction_type == "Flirt":
            interaction_effect = random.randint(10, 30)
            flirt_type = random.choice(list(flirt_types.keys()))
            flirt = random.choice(flirt_types[flirt_type])
            add_message(self, f"I {flirt_type} {person_called}, {flirt}. Romance increased by {interaction_effect}.")
            person.player_romance = min(person.player_romance + interaction_effect, 100)
        else:
            add_message(self, "[event_RED] Invalid interaction type.")

    def death(self, message="I died!"):
        global death_choice, death_msg
        death_choice = True
        death_msg = message

def generate_character(amount=1):
    chars = {}
    for i in range(amount):
        char_gender = random.choice(["male", "female"])
        char_name = generate_random_name(char_gender)
        char = Character(True)
        char.first_name = char_name[0]
        char.last_name = char_name[1]
        char.gender = char_gender.capitalize()
        chars.update({char_name: char})
    return chars

jobs = {
    "Babysitter": Job("Babysitter", "Babysitter", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {"Babysitter": 5000}, 5000),
    "Dog Walker": Job("Dog Walker", "Dog Walker", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {"Dog Walker": 3000}, 3000),
    "Software Developer": Job("Software Developer", "Junior Developer", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Developer": 60000,
        "Mid-level Developer": 80000,
        "Senior Developer": 100000,
        "Lead Developer": 120000,
        "CTO": 200000
    }, 60000),
    "Teacher": Job("Teacher", "Assistant Teacher", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Assistant Teacher": 30000,
        "Teacher": 40000,
        "Senior Teacher": 50000,
        "Head of Department": 60000,
        "Principal": 100000
    }, 30000),
    "Doctor": Job("Doctor", "Intern", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Intern": 50000,
        "Resident": 70000,
        "Attending": 100000,
        "Chief Resident": 120000,
        "Chief of Surgery": 250000
    }, 50000),
    "Lawyer": Job("Lawyer", "Junior Associate", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Associate": 60000,
        "Associate": 80000,
        "Senior Associate": 100000,
        "Partner": 200000,
        "Managing Partner": 300000
    }, 60000),
    "Chef": Job("Chef", "Commis Chef", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Commis Chef": 25000,
        "Chef de Partie": 35000,
        "Sous Chef": 45000,
        "Head Chef": 60000,
        "Executive Chef": 80000
    }, 25000),
    "Artist": Job("Artist", "Apprentice", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Apprentice": 20000,
        "Junior Artist": 30000,
        "Artist": 40000,
        "Senior Artist": 50000,
        "Master Artist": 70000
    }, 20000),
    "Scientist": Job("Scientist", "Research Assistant", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Research Assistant": 40000,
        "Researcher": 60000,
        "Senior Researcher": 80000,
        "Principal Investigator": 100000,
        "Head of Research": 150000
    }, 40000),
    "Police Officer": Job("Police Officer", "Cadet", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Cadet": 30000,
        "Officer": 40000,
        "Sergeant": 50000,
        "Lieutenant": 70000,
        "Chief": 100000
    }, 30000),
    "Nurse": Job("Nurse", "Nursing Assistant", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Nursing Assistant": 30000,
        "Nurse": 40000,
        "Senior Nurse": 50000,
        "Head Nurse": 60000,
        "Director of Nursing": 80000
    }, 30000),
    "Journalist": Job("Journalist", "Junior Reporter", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Reporter": 30000,
        "Reporter": 40000,
        "Senior Reporter": 50000,
        "Editor": 60000,
        "Editor-in-Chief": 100000
    }, 30000),
    "Mechanic": Job("Mechanic", "Apprentice", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Apprentice": 25000,
        "Mechanic": 35000,
        "Senior Mechanic": 45000,
        "Shop Manager": 60000,
        "Garage Owner": 80000
    }, 25000),
    "Electrician": Job("Electrician", "Apprentice", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Apprentice": 25000,
        "Electrician": 35000,
        "Senior Electrician": 45000,
        "Master Electrician": 60000,
        "Electrical Contractor": 80000
    }, 25000),
    "Plumber": Job("Plumber", "Apprentice", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Apprentice": 25000,
        "Plumber": 35000,
        "Senior Plumber": 45000,
        "Master Plumber": 60000,
        "Plumbing Contractor": 80000
    }, 25000),
    "Engineer": Job("Engineer", "Junior Engineer", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Engineer": 60000,
        "Engineer": 80000,
        "Senior Engineer": 100000,
        "Lead Engineer": 120000,
        "Engineering Director": 150000
    }, 60000),
    "Architect": Job("Architect", "Junior Architect", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Architect": 50000,
        "Architect": 70000,
        "Senior Architect": 90000,
        "Lead Architect": 120000,
        "Design Director": 150000
    }, 50000),
    "Accountant": Job("Accountant", "Junior Accountant", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Accountant": 40000,
        "Accountant": 60000,
        "Senior Accountant": 80000,
        "Controller": 100000,
        "CFO": 150000
    }, 40000),
    "Pharmacist": Job("Pharmacist", "Pharmacy Intern", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Pharmacy Intern": 40000,
        "Pharmacist": 60000,
        "Senior Pharmacist": 80000,
        "Pharmacy Manager": 100000,
        "Pharmacy Director": 120000
    }, 40000),
    "Entrepreneur": Job("Entrepreneur", "Startup Founder", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Startup Founder": 0,
        "Small Business Owner": 30000,
        "Medium Enterprise Owner": 70000,
        "Large Enterprise Owner": 150000,
        "CEO": 250000
    }, 0),
    "Photographer": Job("Photographer", "Assistant Photographer", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Assistant Photographer": 20000,
        "Photographer": 30000,
        "Senior Photographer": 50000,
        "Lead Photographer": 70000,
        "Photography Director": 100000
    }, 20000),
    "Pilot": Job("Pilot", "Co-Pilot", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Co-Pilot": 50000,
        "Pilot": 80000,
        "Senior Pilot": 120000,
        "Captain": 150000,
        "Flight Director": 200000
    }, 50000),
    "Real Estate Agent": Job("Real Estate Agent", "Trainee Agent", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Trainee Agent": 20000,
        "Real Estate Agent": 40000,
        "Senior Agent": 60000,
        "Broker": 100000,
        "Real Estate Mogul": 200000
    }, 20000),
    "Dentist": Job("Dentist", "Dental Assistant", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Dental Assistant": 30000,
        "Dentist": 60000,
        "Senior Dentist": 90000,
        "Orthodontist": 120000,
        "Dental Clinic Owner": 150000
    }, 30000),
    "Writer": Job("Writer", "Intern Writer", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Intern Writer": 20000,
        "Staff Writer": 30000,
        "Senior Writer": 50000,
        "Editor": 70000,
        "Author": 100000
    }, 20000),
    "Musician": Job("Musician", "Band Member", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Band Member": 20000,
        "Solo Artist": 40000,
        "Band Leader": 60000,
        "Music Producer": 100000,
        "Music Icon": 200000
    }, 20000),
    "Athlete": Job("Athlete", "Amateur Player", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Amateur Player": 10000,
        "Professional Player": 50000,
        "Team Captain": 100000,
        "League MVP": 150000,
        "Sports Legend": 250000
    }, 10000),
    "Bartender": Job("Bartender", "Barback", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Barback": 20000,
        "Bartender": 30000,
        "Senior Bartender": 40000,
        "Bar Manager": 50000,
        "Bar Owner": 70000
    }, 20000),
    "Fashion Designer": Job("Fashion Designer", "Intern Designer", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Intern Designer": 20000,
        "Junior Designer": 30000,
        "Senior Designer": 50000,
        "Lead Designer": 80000,
        "Fashion Icon": 150000
    }, 20000),
    "Politician": Job("Politician", "Campaign Assistant", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Campaign Assistant": 30000,
        "City Council Member": 50000,
        "Mayor": 80000,
        "Governor": 150000,
        "President": 250000
    }, 30000),
    "Consultant": Job("Consultant", "Junior Consultant", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Consultant": 40000,
        "Consultant": 60000,
        "Senior Consultant": 100000,
        "Partner": 150000,
        "Managing Director": 200000
    }, 40000),
    "Chef": Job("Chef", "Kitchen Porter", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Kitchen Porter": 18000,
        "Line Cook": 25000,
        "Sous Chef": 40000,
        "Head Chef": 60000,
        "Executive Chef": 80000
    }, 18000),
    "Psychologist": Job("Psychologist", "Trainee Psychologist", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Trainee Psychologist": 35000,
        "Psychologist": 50000,
        "Senior Psychologist": 75000,
        "Consultant Psychologist": 100000,
        "Chief Psychologist": 130000
    }, 35000),
    "Zookeeper": Job("Zookeeper", "Assistant Zookeeper", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Assistant Zookeeper": 25000,
        "Zookeeper": 35000,
        "Senior Zookeeper": 45000,
        "Head Zookeeper": 55000,
        "Zoo Director": 75000
    }, 25000),
    "Veterinarian": Job("Veterinarian", "Vet Assistant", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Vet Assistant": 30000,
        "Veterinarian": 60000,
        "Senior Veterinarian": 80000,
        "Vet Clinic Owner": 100000,
        "Chief Veterinarian": 120000
    }, 30000),
    "Animator": Job("Animator", "Junior Animator", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Animator": 25000,
        "Animator": 40000,
        "Senior Animator": 60000,
        "Lead Animator": 80000,
        "Animation Director": 100000
    }, 25000),
    "Game Developer": Job("Game Developer", "Junior Developer", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Developer": 40000,
        "Game Developer": 60000,
        "Senior Developer": 80000,
        "Lead Developer": 100000,
        "Game Director": 150000
    }, 40000),
    "Florist": Job("Florist", "Assistant Florist", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Assistant Florist": 20000,
        "Florist": 30000,
        "Senior Florist": 40000,
        "Florist Shop Owner": 50000,
        "Master Florist": 70000
    }, 20000),
    "Interior Designer": Job("Interior Designer", "Intern Designer", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Intern Designer": 25000,
        "Junior Designer": 40000,
        "Senior Designer": 60000,
        "Lead Designer": 80000,
        "Design Director": 100000
    }, 25000),
    "Baker": Job("Baker", "Apprentice Baker", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Apprentice Baker": 20000,
        "Baker": 30000,
        "Senior Baker": 40000,
        "Pastry Chef": 50000,
        "Bakery Owner": 70000
    }, 20000),
    "IT Specialist": Job("IT Specialist", "Helpdesk Technician", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Helpdesk Technician": 30000,
        "IT Specialist": 45000,
        "Senior IT Specialist": 60000,
        "IT Manager": 80000,
        "CIO": 120000
    }, 30000),
    "PR Manager": Job("PR Manager", "PR Assistant", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "PR Assistant": 25000,
        "PR Executive": 40000,
        "Senior PR Manager": 60000,
        "Head of PR": 80000,
        "PR Director": 100000
    }, 25000),
    "Tour Guide": Job("Tour Guide", "Junior Tour Guide", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Junior Tour Guide": 20000,
        "Tour Guide": 30000,
        "Senior Tour Guide": 40000,
        "Tour Guide Manager": 50000,
        "Tourism Director": 70000
    }, 20000),
    "Translator": Job("Translator", "Intern Translator", random.randint(0, 20), random.randint(30, 100), generate_character(5), generate_character(), {
        "Intern Translator": 25000,
        "Translator": 40000,
        "Senior Translator": 60000,
        "Lead Translator": 80000,
        "Translation Director": 100000
    }, 25000)
}

# Create player character
player = Character()
player.generate_family("player")

# UI Elements positions
header_height = int(50 * HEIGHT / 600)
footer_height = int(50 * HEIGHT / 600)
message_height = HEIGHT - header_height - 2 * footer_height

header_rect = pygame.Rect(0, 0, WIDTH, header_height)
top_footer_rect = pygame.Rect(0, HEIGHT - 2 * footer_height, WIDTH, footer_height)
bottom_footer_rect = pygame.Rect(0, HEIGHT - footer_height, WIDTH, footer_height)
message_rect = pygame.Rect(0, header_height, WIDTH, message_height)

# Buttons
button_width = int(140 * WIDTH / 800)
button_height = int(40 * HEIGHT / 600)
button_gap = int(10 * WIDTH / 800)

career_button_rect = pygame.Rect(button_gap, HEIGHT - 2 * footer_height + 5, button_width, button_height)
assets_button_rect = pygame.Rect(career_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)
age_up_button_rect = pygame.Rect(assets_button_rect.right + button_gap, career_button_rect.top, button_height, button_height)
relationships_button_rect = pygame.Rect(age_up_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)
activities_button_rect = pygame.Rect(relationships_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)

relationship_menu_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
relationship_buttons = {}

prompt_menu_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
prompt_buttons = {}

def add_message(player, msg, msg_type="normal"):
    if msg_type == "normal":
        msg = f"    {msg}"
    player.messages.append(msg)

def display_relationships_menu():
    pygame.draw.rect(screen, LIGHT_BLUE, relationship_menu_rect)
    draw_text(screen, "Relationships", header_font, BLACK, (relationship_menu_rect.x + 10, relationship_menu_rect.y + 10))
    
    y_offset = 60
    people = {**player.relationships, **player.family}

    for i, (name, person) in enumerate(people.items()):
        rel_button_rect = pygame.Rect(relationship_menu_rect.x + 20, relationship_menu_rect.y + y_offset, relationship_menu_rect.width - 50, 40)
        
        # Use a tuple of rectangle coordinates and size as the key
        rel_button_key = (rel_button_rect.x, rel_button_rect.y, rel_button_rect.width, rel_button_rect.height)
        relationship_buttons[rel_button_key] = (rel_button_rect, person)  # Store the rect and the person
        
        
        closeness = person.player_closeness
        romance = person.player_romance
        if person.relationship_with_player not in ["Mother", "Father"]:
            string = f"{name} ({person.relationship_with_player}) - Closeness: {closeness}% - Romance: {romance}%"
        else:
            string = f"{name} ({person.relationship_with_player}) - Closeness: {closeness}%"
        if person.is_jr:
            name = f"{name} Jr."
        elif person.is_sr:
            name = f"{name} Sr."
        draw_button(screen, string, body_font, GREEN, rel_button_rect)
        
        y_offset += 50

def display_choice(prompt, choices, type=None):
    global current_event
    if type == None:
        c1 = GRAY
        c2 = BLACK
        c3 = BLUE
    elif type == "death":
        c1 = BLACK
        c2 = WHITE
        c3 = GRAY
    pygame.draw.rect(screen, c1, prompt_menu_rect)
    draw_text(screen, f"{prompt}", header_font, c2, (prompt_menu_rect.x + 10, prompt_menu_rect.y + 10))
    
    y_offset = 60
    for i, choice in enumerate(choices):
        choice_button_rect = pygame.Rect(prompt_menu_rect.x + 20, prompt_menu_rect.y + y_offset, prompt_menu_rect.width - 50, 40)
        
        # Use a tuple of rectangle coordinates and size as the key
        choice_button_key = (choice_button_rect.x, choice_button_rect.y, choice_button_rect.width, choice_button_rect.height)
        prompt_buttons[choice_button_key] = (choice_button_rect, choice)  # Store the rect and the choice
        
        
        draw_button(screen, choice, body_font, c3, choice_button_rect)
        
        y_offset += 50
    current_event = event

events = [
    # Events for babies (ages 0-4)
    {"age_range": (0, 4), "type": "neutral", "prompt": "I have the chance to speak, what should I say?","descriptions": {"Mama": 'I said, "mama!"', "Dada": 'I said, "dada!"', "Nothin'": 'I chose to stay quite.'}, "custom_effect": False},
    {"age_range": (0, 4), "type": "good", "prompt": "I can get a new toy! What do I choose?","descriptions": {"A robo toy!": 'I got a new robo toy!', "A doll house!": "I got a new doll house!", "Some building blocks!": "I got some new building blocks."}, "effect": {"happiness": 10}, "custom_effect": False},
]

def random_event(player):
    global events, display_choice_active, current_event, pause_active
    
    # Filter events based on age
    available_events = [event for event in events if player.age >= event["age_range"][0] and player.age <= event["age_range"][1]]
    
    event = random.choice(available_events)
    event_effect(event)
    
    display_choice_active = True
    if not pause_active:
        display_choice(event["prompt"], event["descriptions"])
    pause_active = True

def event_effect(event):
    if event["custom_effect"] == True:
        for key, value in event["effect"].items():
            current_value = getattr(player, key)
            if current_value + value > 100:
                setattr(player, key, 100)
            elif current_value + value < 0 and key != "money":
                setattr(player, key, 0)
            else:
                setattr(player, key, current_value + value)

def process_choice(prompt, choice):
    global pause_active
    for event in events:
        if event["prompt"] == prompt and choice in event["descriptions"].keys():
            golobal_event = event
    
    if golobal_event["custom_effect"] == True:
        pass # Make custom logic
    pause_active = False

# Main game loop
running: bool = True
relationships_menu_active: bool = False
death_msg: str = ""
pause_active: bool = False
display_choice_active: bool = False
initial_aged: bool = False
death_choice: bool = False
current_event = None

while running:
    if not initial_aged:
        player.age_up()
        initial_aged = True
    screen.fill(WHITE)

    # Draw Header
    pygame.draw.rect(screen, BLUE, header_rect)
    gender_char = "M" if player.gender == "Male" else "F"
    draw_text(screen, f"{player.first_name} {player.last_name} ({gender_char})", header_font, WHITE, header_rect.move(10, 10))
    draw_text(screen, f"{game_name}", header_font, WHITE, header_rect.move(WIDTH // 2 - 50, 10))
    money_color = GREEN if player.money > 0 else RED
    draw_text(screen, f"Money: ${player.money:,}", header_font, money_color, header_rect.move(WIDTH - 300, 10))

    # Draw Footers
    pygame.draw.rect(screen, BLUE, top_footer_rect)
    pygame.draw.rect(screen, BLUE, bottom_footer_rect)

    # Draw Buttons
    draw_button(screen, "Career", cartoon_font, RED, career_button_rect)
    draw_button(screen, "Assets", cartoon_font, RED, assets_button_rect)
    draw_button(screen, "+", cartoon_font, RED, age_up_button_rect)
    draw_button(screen, "Relationships", cartoon_font, RED, relationships_button_rect)
    draw_button(screen, "Activities", cartoon_font, RED, activities_button_rect)
    
    # Calculate footer height and bar positioning dynamically
    footer_height = int(50 * HEIGHT / 600)
    bar_x_start = int(WIDTH * 0.13)  # Start position X as 13% of the screen width
    bar_y = HEIGHT - int(footer_height * 0.47)  # Lowered the bars closer to the footer

    # Space between bars should be adjusted based on the screen width
    bar_spacing = int(WIDTH * 0.2)  # 20% of the screen width

    # Draw each progress bar with consistent spacing
    draw_progress_bar(screen, bar_x_start, bar_y, WIDTH, HEIGHT, player.health, BLACK)
    draw_progress_bar(screen, bar_x_start + bar_spacing, bar_y, WIDTH, HEIGHT, player.happiness, BLACK)
    draw_progress_bar(screen, bar_x_start + 2 * bar_spacing, bar_y, WIDTH, HEIGHT, player.smarts, BLACK)
    draw_progress_bar(screen, bar_x_start + 3 * bar_spacing, bar_y, WIDTH, HEIGHT, player.looks, BLACK)

    # Define stats
    stats = {
        "Health": player.health,
        "Happiness": player.happiness,  # Fixed typo "Happpiness" -> "Happiness"
        "Smarts": player.smarts,
        "Looks": player.looks
    }

    # Draw Stats
    img_placeholder = f"[IMG]"
    draw_text(screen, img_placeholder, stat_font, BLACK, bottom_footer_rect.move(10, 10))
    
    # Draw health text
    health_txt = f"Health: {player.health}%"
    draw_text(screen, health_txt, stat_font, BLACK, bottom_footer_rect.move(176, 6))
    
    # Draw happiness text
    happiness_txt = f"Happiness: {player.happiness}%"
    draw_text(screen, happiness_txt, stat_font, BLACK, bottom_footer_rect.move(450, 6))
    
    # Draw smarts text
    smarts_txt = f"Smarts: {player.smarts}%"
    draw_text(screen, smarts_txt, stat_font, BLACK, bottom_footer_rect.move(723, 6))
    
    # Draw looks text
    looks_txt = f"Looks: {player.looks}%"
    draw_text(screen, looks_txt, stat_font, BLACK, bottom_footer_rect.move(998, 6))

    # Draw Messages
    for i, msg in enumerate(player.messages[-17:]):
        color_events = {
            "[event_RED]": RED,
            "[event_GREEN]": GREEN,
            "[event_BLUE]": BLUE,
            "[event_ORANGE]": ORANGE,
            "[event_YELLOW]": YELLOW,
            "[event_LIGHT_BLUE]": LIGHT_BLUE,
            "[event_WHITE]": WHITE
        }
        for event_key, color in color_events.items():
            if event_key in msg:
                msg = msg.replace(event_key, "")
                draw_text(screen, msg, body_font, color, message_rect.move(10, 10 + i * 30))
                break
        else:
            draw_text(screen, msg, body_font, BLACK, message_rect.move(10, 10 + i * 30))

    # Handle relationship menu display
    if relationships_menu_active:
        display_relationships_menu()
    
    elif death_choice and not display_choice_active:
        display_choice(death_msg, ["Start a new life.", "Quit game."], "death")

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if relationships_menu_active and not display_choice_active:
                for rel_button_key, (rel_button_rect, person) in relationship_buttons.items():
                    if rel_button_rect.collidepoint(x, y):
                        player.interact_with_relationship(person, "Argue")
                relationships_menu_active = False
            elif display_choice_active:
                for choice_button_key, (choice_button_rect, choice) in prompt_buttons.items():
                    if choice_button_rect.collidepoint(x, y):
                        process_choice(current_event["prompt"], choice)
            elif career_button_rect.collidepoint(x, y):
                add_message(player, "[event_RED] Career feature not implemented yet.")
            elif assets_button_rect.collidepoint(x, y):
                add_message(player, "[event_RED] Assets feature not implemented yet.")
            elif age_up_button_rect.collidepoint(x, y):
                player.age_up()
                prompt_chance = random.randint(1, 100)
                if prompt_chance <= 60:
                    display_choice_active = True
            elif relationships_button_rect.collidepoint(x, y):
                relationships_menu_active = True
            elif activities_button_rect.collidepoint(x, y):
                add_message(player, "[event_RED] Activities feature not implemented yet.")
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            header_height = int(50 * HEIGHT / 600)
            footer_height = int(50 * HEIGHT / 600)
            message_height = HEIGHT - header_height - 2 * footer_height

            header_rect = pygame.Rect(0, 0, WIDTH, header_height)
            top_footer_rect = pygame.Rect(0, HEIGHT - 2 * footer_height, WIDTH, footer_height)
            bottom_footer_rect = pygame.Rect(0, HEIGHT - footer_height, WIDTH, footer_height)
            message_rect = pygame.Rect(0, header_height, WIDTH, message_height)

            button_width = int(140 * WIDTH / 800)
            button_height = int(40 * HEIGHT / 600)
            button_gap = int(10 * WIDTH / 800)

            career_button_rect = pygame.Rect(button_gap, HEIGHT - 2 * footer_height + 5, button_width, button_height)
            assets_button_rect = pygame.Rect(career_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)
            age_up_button_rect = pygame.Rect(assets_button_rect.right + button_gap, career_button_rect.top, button_height, button_height)
            user_stats_button_rect = pygame.Rect(age_up_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)
            other_button_rect = pygame.Rect(user_stats_button_rect.right + button_gap, career_button_rect.top, button_width, button_height)

            header_font = pygame.font.SysFont('comicsansms', int(24 * WIDTH / 800), bold=True)
            body_font = pygame.font.SysFont('comicsansms', int(18 * WIDTH / 800))
            cartoon_font = pygame.font.SysFont('comicsansms', int(24 * WIDTH / 800))

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()
