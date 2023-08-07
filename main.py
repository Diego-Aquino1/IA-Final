import random

def calculate_distance(articles):
    total_distance = 0
    prev_item = 0
    
    for item in articles:
        total_distance += abs(item - prev_item)
        prev_item = item
    
    return total_distance

def fcfs_algorithm(orders, n_capacidad):
    lotes = []
    lote_actual = []
    capacidad_actual = 0
    distancia_total = 0
    
    for orden, capacidad, articles in orders:
        distancia_total += calculate_distance(articles)
        if capacidad_actual + capacidad <= n_capacidad:
            lote_actual.append((orden, capacidad, articles))
            capacidad_actual += capacidad
        else:
            lote_encontrado = False
            for lote in lotes:
                if sum([capacidad for _, capacidad, _ in lote]) + capacidad <= n_capacidad:
                    lote.append((orden, capacidad, articles))
                    capacidad_actual += capacidad
                    lote_encontrado = True
                    break
            if not lote_encontrado:
                lotes.append(lote_actual)
                lote_actual = [(orden, capacidad, articles)]
                capacidad_actual = capacidad
        
    if lote_actual:
        lotes.append(lote_actual)
    
    return lotes, distancia_total

def generate_orders(num_ordenes, n_capacidad):
    orders = []
    for i in random.sample(range(1, num_ordenes + 1), num_ordenes):
        capacidad = random.randint(3, n_capacidad)
        articles = random.sample(range(1, 901), capacidad)
        orders.append((i, capacidad, articles))
    return orders

def fitness(individual):
    _, distancia_total = fcfs_algorithm(individual, n_capacidad)
    return distancia_total

def select_parents(population, fitness_values, n_parents):
    parents = []
    max_fitness = max(fitness_values)
    normalized_fitness = [max_fitness - fit for fit in fitness_values]
    total_fitness = sum(normalized_fitness)
    
    for _ in range(n_parents):
        threshold = random.uniform(0, total_fitness)
        acc_fitness = 0
        for i, fit in enumerate(normalized_fitness):
            acc_fitness += fit
            if acc_fitness >= threshold:
                parents.append(population[i])
                break
    return parents

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual):
    if random.random() < 0.1:
        index1 = random.randint(0, len(individual) - 1)
        index2 = random.randint(0, len(individual) - 1)
        individual[index1], individual[index2] = individual[index2], individual[index1]

def create_population_sin_pesos(population_):
    return [[orden for orden, _, _ in lista] for lista in population_]

# Lista de combinaciones de parámetros iniciales
param_combinations = [
    (20, 25), (20, 50), (20, 100),
    (40, 25), (40, 50), (40, 100),
    (80, 25), (80, 50), (80, 100),
    (100, 25), (100, 50), (100, 100)
]

for params in param_combinations:
    # Parámetros iniciales
    num_ordenes, n_capacidad = params
    n_poblacion = int(20 + num_ordenes / 2)
    n_parents = int(n_poblacion * 0.9)
    n_iterations = int(40 + num_ordenes / 3)

    # Generar población inicial (listas de órdenes sin pesos ni items)
    population = [generate_orders(num_ordenes, n_capacidad) for _ in range(n_poblacion)]

    # Crear archivo de texto
    output_file = open(f"genetic_algorithm_results_{num_ordenes}_{n_capacidad}.txt", "w")

    # Algoritmo genético
    for iteration in range(n_iterations):
        fitness_values = [fitness(individual) for individual in population]
        parents = select_parents(population, fitness_values, n_parents)
        next_population = parents.copy()

        # Detalles de la iteración
        output_file.write(f"Iteracion {iteration + 1}:\n")
        output_file.write("Poblacion:\n")
        
        for i, individual in enumerate(create_population_sin_pesos(population)):
            output_file.write(f"Individuo {i + 1}: {individual} - Fitness: {fitness_values[i]}\n")

        while len(next_population) < n_poblacion:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            output_file.write(f"Seleccion de padres: {parent1} y {parent2}\n")
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            next_population.append(child1)
            next_population.append(child2)
            output_file.write(f"Cruzamiento y mutacion: {child1} y {child2}\n")

        population = next_population

    # Cerrar archivo de texto
    output_file.close()

    print(f"Proceso completado para num_ordenes = {num_ordenes}, n_capacidad = {n_capacidad}.")

