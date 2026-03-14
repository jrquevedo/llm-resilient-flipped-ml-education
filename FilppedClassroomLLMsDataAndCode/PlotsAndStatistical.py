import random
import numpy as np

# Params
years =[2025,2026] # Academic year
colors=['tab:blue','tab:orange']
nPA   =10          # Number of practical activities (PA)
seed  =2480
meanPA=[5,8,4,7,5,6,9,9,4,7] # Mean of each PA

outTableLaTex='AvgPA.tex'

# Main Program

import pandas as pd
import numpy as np

def read_grades(csv_file):
    """
    Reads a CSV file with PA columns and a final grade column.
    Returns:
        num_students : total number of rows in the CSV
        pa_arrays    : list of numpy arrays with existing values of each PA
        final_grades : numpy array with existing final grades
    """

    df = pd.read_csv(csv_file)

    # number of students (rows in the file)
    num_students = len(df)

    # detect PA columns and sort them (PA1..PA10)
    pa_columns = sorted(
        [col for col in df.columns if col.startswith("PA")],
        key=lambda x: int(x[2:])
    )

    # build arrays removing NaN values
    pa_arrays = [df[col].dropna().to_numpy() for col in pa_columns]

    # final grades (last column), removing NaN
    final_grades = df.iloc[:, -1].dropna().to_numpy()

    return num_students, pa_arrays, final_grades


PAMeans =[]
PACounts=[]
finalTooks=[]

for year in years: 
    
    [nstudents,pa_arrays,finalTook]=read_grades('assessments{}.csv'.format(year))
    nPA=len(pa_arrays)
    nWithdraw=nstudents-len(finalTook)
    
    print('\nYear: {}'.format(year))
    print('NInitial: {}'.format(nstudents))
    print('Course completion: {}'.format(len(finalTook)))
    print('Grade Avg.:{:4.2f} Variance:{:4.2f} '.
          format(np.mean(finalTook),np.var(finalTook)))
    
    PASum  =[sum(PA) for PA in pa_arrays]
    PACount=[len(PA) for PA in pa_arrays]
    
    PAMean=[PASum[j]/PACount[j] for j in range(nPA)]
    for j in range(nPA):
        print('PA{} Mean={:4.2f} N={}'.format(j+1,PAMean[j],PACount[j]))
        
    finalTooks.append(finalTook)
    PAMeans.append(PAMean)
    PACounts.append(PACount)


#%% Wilcoxon signed-rank
from scipy.stats import wilcoxon

Y25=PAMeans[0]
Y26=PAMeans[1]
stat, p_value = wilcoxon(Y25,Y26)
print('Wilcoxon signed-rank stat={:g} p_value={}'.format(stat,p_value))

# LaTex
print('\\begin{table}[h]\n\\centering\n\\small\n\\begin{tabular}{lccc}\n\\hline')
print('PA&2024--2025&2025--2026&sign\\\\ \\hline')
for ipa in range(nPA):
    print('PA{}&{:4.2f}&{:4.2f}&${}$ \\\\'.format(ipa+1,Y25[ipa],Y26[ipa],'+' if Y26[ipa]>Y25[ipa] else '-'))
print(' \\hline \\end{tabular}')
print('\\caption{Average grades for each practical activity (PA) in the 2024--2025 and 2025--2026 academic years. For each PA, the sign indicates whether the 2025--2026 mean is higher than the 2024--2025 mean.}')
print('\\label{tab:avgPA}')
print('\\end{table}')

#%% Graph showing student Course Completion per Practical Activity (Absolute and percent)
import matplotlib.pyplot as plt

header=['{}--{}'.format(y-1,y) for y in years]
dataNames=['PA{}'.format(j+1) for j in range(nPA)]

# Absolute values
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True,gridspec_kw={'hspace': 0.05})
ax1.set_ylim(54,76)
ax1.set_yticks(list(range(55,76,5)))
for iy in range(len(years)):
    ax1.plot(dataNames,PACounts[iy],marker='+',label=header[iy],color=colors[iy])
ax1.legend()
ax1.grid()
ax1.set_ylabel('Course Completion')
for iy in range(len(years)):
    # Calculating the percent
    s=PACounts[iy][0]
    PAPer=[100*v/s for v in PACounts[iy]]
    ax2.plot(dataNames,PAPer,marker='+',label=header[iy],color=colors[iy])
ax2.legend()
ax2.set_ylim(70,105)
nyticks=[75,80,85,90,95,100]
syticks=['{}%'.format(v) for v in nyticks]
ax2.set_yticks(nyticks,syticks)
ax2.grid()
ax2.set_ylabel('Course Completion (%)')

ax2.set_xlabel('Practical Activity')
fig.savefig('CourComplePA.pdf',bbox_inches='tight')
    
#%% Proportion of students
bins=[0,5,7,8,9,10]
plt.figure()
plt.xticks(bins)
# plt.ylim(0,30)
for iy in range(len(years)):
    counts, _ = np.histogram(finalTooks[iy], bins=bins,density=True)
    counts=counts*100
    X=[]
    Y=[]
    for ib in range(len(bins)-1):
        x1=bins[ib]
        x2=bins[ib+1]
        y=counts[ib]
        X=X+[x1,x1,x2,x2]
        Y=Y+[0,y,y,0]
    posiciones=list(range(0,41,5))
    etiquetas =['{}%'.format(p) for p in posiciones]
    plt.yticks(posiciones, etiquetas)
    plt.plot(X,Y,label=header[iy],color=colors[iy])
plt.legend()
plt.grid(axis='y')
plt.ylabel('Proportion of students')
plt.xlabel('Grade intervals')
plt.savefig('PropFinalGrades.pdf')
 
#%% Welch’s t-test de las notas finales (Suponer diferente varianza)
from scipy.stats import ttest_ind

# 1. Creamos datos de muestra (con varianzas visiblemente distintas)
grupo_a = finalTooks[0]
grupo_b = finalTooks[1]

print('\nFinal Exam grades:')
print('2024-2025 N={} Mean={:5.2f} Variance={:5.4f}'.format(len(grupo_a),np.mean(grupo_a),np.var(grupo_a)))
print('2025-2026 N={} Mean={:5.2f} Variance={:5.4f}'.format(len(grupo_b),np.mean(grupo_b),np.var(grupo_b)))

# 2. Ejecutamos el Welch's t-test
# Nota: equal_var=False es lo que activa el t-test de Welch
t_stat, p_valor = ttest_ind(grupo_a, grupo_b, equal_var=False)

print('Welch''s t-test')
print(f" Estadistical t: {t_stat:.4f}")
print(f" P-value: {p_valor:.4f}")


def get_welch_df(x, y):
    n1, n2 = len(x), len(y)
    v1, v2 = np.var(x, ddof=1), np.var(y, ddof=1)
    
    # Numerador
    num = (v1/n1 + v2/n2)**2
    # Denominador
    den = (v1/n1)**2 / (n1 - 1) + (v2/n2)**2 / (n2 - 1)
    
    return num / den

df = get_welch_df(grupo_a, grupo_b)
print(f" Degrees of freedom: {df:.4f}")

# 3. Interpretación rápida
if p_valor < 0.05:
    print(" There is a statistically significant difference between the groups.")
else:
    print(" There is not enough evidence to conclude that the groups are different.")



def hedges_g(x, y):
    n1, n2 = len(x), len(y)
    v1, v2 = np.var(x, ddof=1), np.var(y, ddof=1)
    
    # 1. Desviación estándar combinada (pooled)
    s_p = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    
    # 2. d de Cohen inicial
    d = (np.mean(x) - np.mean(y)) / s_p
    
    # 3. Factor de corrección de Hedges
    correction = 1 - (3 / (4 * (n1 + n2) - 9))
    
    return d * correction

g=hedges_g(grupo_a,grupo_b)
print('\nHedges g={}'.format(g))

#%% Notas de teoría para comparar
print('\nTheoretical grades')
notas24_25 = [5.4, 5.25, 2.18, 2.23, 3.38, 1.28, 4.25, 4.23, 5.38, 1.18, 4.0, 1.63, 4.23, 5.03,6.95, 4.08, 5.5, 5.73, 5.15,4.33, 4.75, 3.78, 8.33, 5.28, 7.43, 6.13, 4.28, 3.35, 1.35, 3.25, 2.35, 3.83, 4.88, 0.45, 6.15, 4.73, 8.58,6.9, 9.35, 0.55, 2.05, 5.85, 7.85, 6.18, 4.25]
notas25_26 = [4.98, 7.08, 7.58, 3.35, 5.05, 2.63, 5.15, 9.05, 4.15, 1.98, 4.1, 4.05, 5.58, 4.15, 6.33, 2.45, 2.83, 6.88, 5.2, 3.48, 4.05, 6.05, 9.18, 4.18, 2.68, 2.85, 4.73, 4.05, 4.73, 4.8,  4.4, 4.53, 4.05, 3.38, 4.3, 4.53, 1.43, 1.45, 4.0, 6.58, 3.08, 2.33, 4.15, 4.53, 5.98, 7.35, 1.83, 7.5, 2.63, 4.75, 3.1, 4.0]

# 1. Creamos datos de muestra (con varianzas visiblemente distintas)
grupo_a = notas24_25
grupo_b = notas25_26

print('\nFinal Exam grades:')
print('2024-2025 N={} Mean={:5.2f} Variance={:5.4f}'.format(len(grupo_a),np.mean(grupo_a),np.var(grupo_a)))
print('2025-2026 N={} Mean={:5.2f} Variance={:5.4f}'.format(len(grupo_b),np.mean(grupo_b),np.var(grupo_b)))

# 2. Ejecutamos el Welch's t-test
# Nota: equal_var=False es lo que activa el t-test de Welch
t_stat, p_valor = ttest_ind(grupo_a, grupo_b, equal_var=False)

print('Welch''s t-test')
print(f" Estadístical t: {t_stat:.4f}")
print(f" P-value: {p_valor:.4f}")


def get_welch_df(x, y):
    n1, n2 = len(x), len(y)
    v1, v2 = np.var(x, ddof=1), np.var(y, ddof=1)
    
    # Numerador
    num = (v1/n1 + v2/n2)**2
    # Denominador
    den = (v1/n1)**2 / (n1 - 1) + (v2/n2)**2 / (n2 - 1)
    
    return num / den

df = get_welch_df(grupo_a, grupo_b)
print(f" Degrees of freedom:: {df:.4f}")

# 3. Interpretación rápida
if p_valor < 0.05:
    print(" There is a statistically significant difference between the groups")
else:
    print(" There is not enough evidence to conclude that the groups are different.")



def hedges_g(x, y):
    n1, n2 = len(x), len(y)
    v1, v2 = np.var(x, ddof=1), np.var(y, ddof=1)
    
    # 1. Desviación estándar combinada (pooled)
    s_p = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    
    # 2. d de Cohen inicial
    d = (np.mean(x) - np.mean(y)) / s_p
    
    # 3. Factor de corrección de Hedges
    correction = 1 - (3 / (4 * (n1 + n2) - 9))
    
    return d * correction

g=hedges_g(grupo_a,grupo_b)
print('\nHedges g={}'.format(g))





    