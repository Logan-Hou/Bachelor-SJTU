import pandas as pd
from class_mirror import mirror, normalize_vector
import itertools
from eta_sb import *
import warnings
import time
from get_mirros_pos import get_mirrors_pos

def dni(sin_alpha_s):
    g0 = 1366
    H = 3
    a = 0.4237 - 0.000821*((6-H)**2)
    b = 0.5055 + 0.00595*((6.5-H)**2)
    c = 0.2711 + 0.01858*((2.5-H)**2)
    dni = g0 * (a+b*math.exp(-c/sin_alpha_s))
    return dni


# 定义适应度函数（目标函数）
def objective_function(r1, r2, r3, r4, c1,  c2, c3, c4,w1, w2, w3, w4, h1, h2, h3, h4 ,y_tower):
    hours = [9, 10.5, 12, 13.5, 15]
    dates = [f"2022{str(i).rjust(2,'0')}21" for i in range(3,5)]

    df_get_mirrors_pos = get_mirrors_pos(r1,r2,r3,r4,c1,c2,c3,c4,
                                w1,w2,w3,w4,h1,h2,h3,h4,y_tower)  # 得到每个镜子初始化坐标初始化
    df = df_get_mirrors_pos.copy()

    df.columns = ['x', 'y','c','w','h']
    df['(x,y)'] = list(zip(df['x'],df['y'],df.index+1))
    df['id'] = df.index+1
    date_mean_table = pd.DataFrame({'hour': [], 'eta': [], 'eta_cos': [], 'eta_sb': [], 'eta_trunc': [], 'Efield': [], 'Efield_mirror_mean': []})
    hour_mean_table = {'hour': [], 'eta': [], 'eta_cos': [], 'eta_sb': [], 'eta_trunc': [], 'Efield': [],
                       'Efield_mirror_mean': []}

    df['mirrors'] = df.apply(lambda x: mirror(x['(x,y)'][2], x['(x,y)'][0], x['(x,y)'][1],x['c'],x['w'],x['j']))
    mirror_list = list(df['mirrors'])
    df['mirrors'] = df['mirrors'].apply(lambda x: mirror.top5_close(x, mirror_list))
    E_field = []
    for date, hour in itertools.product(dates, hours):
        print('date',date)
        sun_vec = sun_vector(hour, phi=39.4, date=date)
        sin_alpha_s = sun_vector(hour, date=date, askfor='sin_alpha_s', phi=39.4)
        sin_gamma_s,cos_gamma_s,tan_alpha_s = sun_vector(hour, phi=39.4, date=date, askfor='alpha_gamma_s')
        r_shadow = np.array([-sin_gamma_s, -cos_gamma_s, 0])
        l_shadow = np.array([cos_gamma_s,-sin_gamma_s,0])

        df['normal_vec'] = df['mirrors'].apply(lambda x: mirror.normal_vector(x, sun_vec))
        df['eta_cos'] = df['mirrors'].apply(lambda x: mirror.eta_cos(x, sun_vec))
        df['eta_at'] = df['mirrors'].apply(lambda x: eta_at(x.d_hr))
        df['mirror_i_loc'] = df['mirrors'].apply(lambda x: x.mirror_loc)
        df['mirror_area'] = df['mirrors'].apply(lambda x: x.area)

        df['eta_sb_trunc'] = df.apply(lambda x: eta_sb(x['mirrors'], sun_vec, r_shadow, l_shadow, tan_alpha_s, width=x['w'], height=x['h'], center_z=x['c']),axis=1)            # todo get a series

        df['eta_sb'] = df['eta_sb_trunc'].apply(lambda x: x[0])
        df['eta_trunc'] = df['eta_sb_trunc'].apply(lambda x: x[1])
        df['eta'] = df['eta_sb']*df['eta_at']*df['eta_cos']*df['eta_trunc']*0.92
        E_field.append(dni(sin_alpha_s)*sum(df['mirror_area']*df['eta']))
    E_field_mean = pd.Series(E_field).mean()
    return E_field_mean


# PSO-GA算法
def pso_ga(objective_function, num_particles, num_dimensions, max_iterations,
           m, c1, c2, Pc, Pm):
    # 初始化粒子群和GA种群
    swarm_position = np.random.rand(num_particles, num_dimensions)
    swarm_velocity = np.random.rand(num_particles, num_dimensions)
    ga_population = np.random.rand(num_particles, num_dimensions)


    best_swarm_position = swarm_position.copy()
    best_swarm_value = np.zeros(num_particles)

    for i in range(num_particles):
        r1, c1, w1, h1, y_tower = list(swarm_position[i])
        r1, r2, r3, r4 = [r1] * 4
        c1, c2, c3, c4 = [c1] * 4
        w1, w2, w3, w4 = [w1] * 4
        h1, h2, h3, h4 = [h1] * 4
        best_swarm_value[i] = objective_function(r1, r2, r3, r4,  c1, c2, c3, c4,w1, w2, w3, w4, h1, h2, h3, h4, y_tower)

    global_best_index = np.argmin(best_swarm_value)
    global_best_position = swarm_position[global_best_index]
    global_best_value = best_swarm_value[global_best_index]

    for iteration in range(max_iterations):
        for i in range(num_particles):
            current_value = objective_function(swarm_position[i])

            if current_value < best_swarm_value[i]:
                best_swarm_position[i] = swarm_position[i]
                best_swarm_value[i] = current_value

            if current_value < global_best_value:
                global_best_position = swarm_position[i]
                global_best_value = current_value

            r1, r2 = np.random.rand(), np.random.rand()
            swarm_velocity[i] = (m * swarm_velocity[i] +
                                  c1 * r1 * (best_swarm_position[i] - swarm_position[i]) +
                                  c2 * r2 * (global_best_position - swarm_position[i]))
            swarm_position[i] += swarm_velocity[i]

        selected_parents = np.random.choice(num_particles, num_particles // 2, replace=True)
        offspring = []
        for i in range(0, num_particles, 2):
            parent1, parent2 = selected_parents[i], selected_parents[i + 1]
            crossover_point = np.random.randint(num_dimensions)
            child1 = np.concatenate((ga_population[parent1][:crossover_point], ga_population[parent2][crossover_point:]))
            child2 = np.concatenate((ga_population[parent2][:crossover_point], ga_population[parent1][crossover_point:]))
            offspring.extend([child1, child2])

        offspring = np.array(offspring)

        crossover_mask = np.random.rand(num_particles, num_dimensions) < Pc
        ga_population[crossover_mask] = offspring[crossover_mask]

        mutation_mask = np.random.rand(num_particles, num_dimensions) < Pm
        mutation_values = np.random.rand(num_particles, num_dimensions)
        ga_population[mutation_mask] = mutation_values[mutation_mask]
    return global_best_position, global_best_value


def main():
    num_particles = 20
    num_dimensions = 5
    max_iterations = 100
    m = 0.5
    c1 = 1.5
    c2 = 1.5
    Pc = 0.8
    Pm = 0.3

    best_position, best_value = pso_ga(objective_function, num_particles, num_dimensions, max_iterations,
                                       m, c1, c2, Pc, Pm)
    series = pd.Series(best_position,best_position)
    series.to_csv('result.csv')
if __name__ == '__main__':
    main()