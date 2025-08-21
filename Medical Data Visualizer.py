import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Load data
df = pd.read_csv('medical_examination.csv')

# 2. Add overweight column (binarized)
df['overweight'] = (df['weight'] / ((df['height']/100)**2) > 25).astype(int)

# 3. Normalize cholesterol and glucose to 0/1
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4. Draw categorical plot
def draw_cat_plot():
    # Melt dataframe to long format
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol','gluc','smoke','alco','active','overweight']
    )

    # Add count column and group
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio','variable','value'], as_index=False).count()

    # Draw bar plot using seaborn
    fig = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar'
    ).fig

    # Save figure
    fig.savefig('catplot.png')
    return fig

# 5. Draw heatmap
def draw_heat_map():
    # Clean data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate correlation matrix
    corr = df_heat.corr()

    # Generate mask for upper triangle
    mask = np.triu(corr)

    # Draw heatmap
    fig, ax = plt.subplots(figsize=(12,12))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        linewidths=1,
        square=True,
        center=0,
        cbar_kws={'shrink':0.5}
    )

    # Save figure
    fig.savefig('heatmap.png')
    return fig
