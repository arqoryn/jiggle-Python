"""
Population Dynamics Simulation (Agent-Based Demographic Model)
Author: Mohamad Musadiq (@arqoryn)
Date Last Modified: 06/02/2026

This program simulates the evolution of a human population over discrete
time steps (each step representing 5 years). Individuals are modeled as
agents stored in a CSV file and loaded into memory for each simulation
cycle. The system updates demographic characteristics such as age,
fertility, partnerships, reproduction, and mortality, then persists the
updated state back to disk.

Core Features
-------------
- CSV-based persistent population storage
- Randomized initial population generation
- Age progression across time steps
- Age-dependent fertility activation and decline
- Random pairing of single individuals into couples
- Ongoing reproduction among all existing couples
- Age-dependent mortality probabilities
- Census tracking of living population size

Simulation Flow (Per Time Step)
-------------------------------
1. Load existing population from CSV (or generate an initial population).
2. Apply mortality rules based on age-dependent probabilities.
3. Age all living individuals by one simulation interval (5 years).
4. Update fertility status based on age thresholds.
5. Identify single individuals and form new partnerships.
6. Retrieve all current couples and simulate reproduction.
7. Append newborn individuals to the population.
8. Save the updated population back to the CSV file.

Data Representation
-------------------
Each individual is represented as a dictionary with the following fields:
    id               : Unique identifier
    sex              : 'M' or 'F'
    age              : Age in years
    alive            : 1 (alive) or 0 (deceased)
    health           : Health score (0–100)
    fertility        : 1 (fertile) or 0 (infertile)
    partner_id       : ID of current partner or -1 if single
    children_count   : Number of children produced

Purpose
-------
This project demonstrates a simple agent-based demographic simulation
framework suitable for experimentation with population growth,
mortality/fertility parameters, and long-term demographic dynamics.
"""

import random

FILE_PATH = "simulation\\individual.csv"


# --------------------------------------------------
# Load population from CSV into memory
# --------------------------------------------------
def load_population():
    population = []

    with open(FILE_PATH, "r") as f:
        lines = f.readlines() # one big list as all the lines as elements

    for line in lines[1:]:  # skip header
        line = line.strip()  # remove '\n'
        if line == "":      # remove empty lines (safety)
            continue 

        item = line.split(",") # a list for each line => item = ['0','M','33','1','73','1','8','0']

        # store the list items in the dictionary
        person = {
            "id": int(item[0]),
            "sex": item[1],
            "age": int(item[2]),
            "alive": int(item[3]),
            "health": int(item[4]),
            "fertility": int(item[5]),
            "partner_id": int(item[6]),
            "children_count": int(item[7])
        }

        # add the dictionary into the list => population = []
        population.append(person)

    return population # (a list of multiple dictionaries)


# --------------------------------------------------
# Save population back to CSV
# --------------------------------------------------
def save_population(population):
    # open file in write mode, clears old content
    with open(FILE_PATH, "w") as f:
        f.write("id,sex,age,alive,health,fertility,partner_id,children_count\n") # write header separately

        # turn each dictionary values into a csv line (f-string)
        for p in population:
            line = f"{p['id']},{p['sex']},{p['age']},{p['alive']},{p['health']},{p['fertility']},{p['partner_id']},{p['children_count']}\n"

            f.write(line)


# --------------------------------------------------
# Generate initial population
# --------------------------------------------------
def generate_initial_population():
    population = []
    next_id = 0

    for i in range(10):
        population.append({
            "id": next_id,
            "sex": "M",
            "age": random.randint(18, 40),
            "alive": 1,
            "health": random.randint(70, 100),
            "fertility": 1,
            "partner_id": -1,
            "children_count": 0
        })
        next_id += 1

    for i in range(10):
        population.append({
            "id": next_id,
            "sex": "F",
            "age": random.randint(18, 40),
            "alive": 1,
            "health": random.randint(70, 100),
            "fertility": 1,
            "partner_id": -1,
            "children_count": 0
        })
        next_id += 1

    return population


# --------------------------------------------------
# Get single men and women
# --------------------------------------------------
def get_single_people(population):
    singleMen = []
    singleWomen = []

    for p in population:
        if p["alive"] == 1 and p["partner_id"] == -1:
            if p["sex"] == "M":
                singleMen.append(p)
            elif p["sex"] == "F":
                singleWomen.append(p)

    return singleMen, singleWomen


# --------------------------------------------------
# Pair men and women
# --------------------------------------------------
def pair_people(singleMen, singleWomen):
    random.shuffle(singleMen)
    random.shuffle(singleWomen)

    pairs = []
    count = min(len(singleMen), len(singleWomen))

    for i in range(count):
        pairs.append((singleMen[i], singleWomen[i]))

    return pairs


# --------------------------------------------------
# Apply pairing
# --------------------------------------------------
def apply_pairs(pairs):
    for man, woman in pairs:
        man["partner_id"] = woman["id"]
        woman["partner_id"] = man["id"]

# --------------------------------------------------
# Get All Couples
# --------------------------------------------------

def get_all_couples(population):
    couples = []
    visited = set()

    for p in population:
        if p["partner_id"] != -1 and p["id"] not in visited:
            partner = next(x for x in population if x["id"] == p["partner_id"])
            couples.append((p, partner))
            visited.add(p["id"])
            visited.add(partner["id"])

    return couples

# --------------------------------------------------
# Reproduction logic
# --------------------------------------------------
def reproduce(population, get_all_couples):
    next_id = max(p["id"] for p in population) + 1   # generator expression: find max + 1 of all id's in population
    new_children = []
    
    for man, woman in get_all_couples:
        if man["alive"] == 1 and woman["alive"] == 1:
            if man["fertility"] == 1 and woman["fertility"] == 1:
                if random.random() < 0.5:  # 50 percent chance
                    sex = "M" if random.randint(0, 1) == 1 else "F"   # ternary expression: 'A' if <condition == True> else 'B' 

                    child = {
                        "id": next_id,
                        "sex": sex,
                        "age": 0,
                        "alive": 1,
                        "health": random.randint(70, 100),
                        "fertility": 0,
                        "partner_id": -1,
                        "children_count": 0
                    }

                    man["children_count"] += 1
                    woman["children_count"] += 1

                    new_children.append(child)
                    next_id += 1

    population.extend(new_children)


# --------------------------------------------------
# Aging logic
# --------------------------------------------------
def aging_update(population):
    for p in population:
        if p["alive"] == 1:     # only age if alive
            p["age"] += 5

# --------------------------------------------------
# Death logic
# --------------------------------------------------
def death(population):
    for p in population:
        if p["age"] < 1:
            death_prob = random.random()
            if death_prob < 0.05:
                p["alive"] = 0
        if p["age"] < 15 and p["age"] > 1:
            death_prob = random.random()
            if death_prob < 0.01:
                p["alive"] = 0
        elif p["age"] < 40 and p["age"] > 15:
            death_prob = random.random()
            if death_prob < 0.005:
                p["alive"] = 0
        elif p["age"] < 55 and p["age"] > 40:
            death_prob = random.random()
            if death_prob < 0.02:
                p["alive"] = 0
        elif p["age"] < 70 and p["age"] > 55:
            death_prob = random.random()
            if death_prob < 0.05:
                p["alive"] = 0
        elif p["age"] < 85 and p["age"] > 70:
            death_prob = random.random()
            if death_prob < 0.15:
                p["alive"] = 0
        elif p["age"] >= 85:
            death_prob = random.random()
            if death_prob < 0.35:
                p["alive"] = 0
        
# --------------------------------------------------
# Population Counter
# --------------------------------------------------
def census(population):
        census = 0
        for p in population:
            if p["alive"] == 1:
                census += 1
        
        return census

# --------------------------------------------------
# Update Fertility
# --------------------------------------------------
def fertility_update(population):
    for p in population:
        if p["age"] > 18 and p["fertility"] == 0:
            p["fertility"] = 1

        if p["age"] > 65:
            p["fertility"] = 0
        
# --------------------------------------------------
# MAIN DRIVER
# --------------------------------------------------
def main():
    year = 0

    while True:
        try:
            population = load_population()
            if len(population) == 0:
                raise FileNotFoundError
        except:
            population = generate_initial_population()
            save_population(population)



        print("=== Step DATA ===")
        print("Year: ", year)
        tot = census(population)
        print("Total Population: ", tot)
        inp = input("Press Enter to forward to next event (10 Years): ")


        if inp == "":
            death(population)
            aging_update(population)
            fertility_update(population)
            men, women = get_single_people(population)
            pairs = pair_people(men, women)
            apply_pairs(pairs)

            all_couples = get_all_couples(population)
            reproduce(population, all_couples)

            year += 5
            save_population(population)
            print("Simulation step complete")


main()
