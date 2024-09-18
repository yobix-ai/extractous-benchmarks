#!/usr/bin/env python
import sys

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


# Generic function to plot grouped bar charts
def plot_grouped_bar_chart(df, column, results_dir, colors, title, ylabel, filename):
    # Group by 'file' and 'script' to get the values for the specified column
    grouped = df.groupby(['file', 'script'])[column].mean().reset_index()

    # Extract unique files and scripts
    unique_files = grouped['file'].unique()
    unique_scripts = grouped['script'].unique()

    # Set up the bar positions
    bar_width = 0.2  # Width of each bar
    x = np.arange(len(unique_files))  # X locations for the groups

    # Plotting
    plt.figure(figsize=(14, 8))

    for i, script in enumerate(unique_scripts):
        # Extract data for the current script
        script_data = grouped[grouped['script'] == script]

        # Get the column values in the order of unique_files
        values = [script_data[script_data['file'] == f][column].values[0] if f in script_data['file'].values else 0 for
                  f in unique_files]

        # Plot bars for this script with a specific color
        plt.bar(x + i * bar_width, values, bar_width, label=script,
                color=colors.get(script, 'gray'))  # Default to 'gray' if script not in colors

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(x + bar_width, unique_files, rotation=45, ha="right")
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.30), ncol=len(unique_scripts))
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, filename))  # Save plot in the results directory
    plt.close()


# Generic function to plot grouped bar charts with overall averages
def plot_grouped_bar_chart_with_overall(df, column, results_dir, colors, title, ylabel, filename):
    # Group by 'file' and 'script' to get the values for the specified column
    grouped = df.groupby(['file', 'script'])[column].mean().reset_index()

    # Calculate overall average for each script
    overall_avg = grouped.groupby('script')[column].mean().reset_index()
    overall_avg['file'] = 'Overall Average'  # Add a label for overall averages

    # Concatenate both DataFrames
    combined_df = pd.concat([grouped, overall_avg], ignore_index=True)

    # Extract unique files and scripts
    unique_files = combined_df['file'].unique()
    unique_scripts = combined_df['script'].unique()

    # Set up the bar positions
    bar_width = 0.2  # Width of each bar
    x = np.arange(len(unique_files))  # X locations for the groups

    # Plotting
    plt.figure(figsize=(14, 8))

    for i, script in enumerate(unique_scripts):
        # Extract data for the current script
        script_data = combined_df[combined_df['script'] == script]

        # Get the column values in the order of unique_files
        values = [script_data[script_data['file'] == f][column].values[0] if f in script_data['file'].values else 0 for
                  f in unique_files]

        # Plot bars for this script with a specific color
        plt.bar(x + i * bar_width, values, bar_width, label=script,
                color=colors.get(script, 'gray'))  # Default to 'gray' if script not in colors

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(x + bar_width, unique_files, rotation=45, ha="right")
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.30), ncol=len(unique_scripts))
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, filename))  # Save plot in the results directory
    plt.close()


# Generic function to plot speed-up per file with grouped bars and overall average
def plot_grouped_bar_chart_speedup_with_overall(df, column, results_dir, colors, title, ylabel, filename, reference_script):
    # Create a new DataFrame to store speed-up values
    speedup_values = []

    # Group by 'file' and 'script' to get the values for the specified column
    grouped = df.groupby(['file', 'script'])[column].mean().reset_index()

    # Get the reference times (values of the reference script)
    reference_values = grouped[grouped['script'] == reference_script].set_index('file')[column].to_dict()

    # Calculate the speed-up for each script relative to the reference script
    for script in df['script'].unique():
        for file in df['file'].unique():
            # Get the value of the current script for the current file
            script_value = grouped[(grouped['file'] == file) & (grouped['script'] == script)][column].values

            # If both the script value and reference value exist, calculate speed-up
            if len(script_value) > 0 and file in reference_values:
                speedup = reference_values[file] / script_value[0]
                speedup_values.append({'file': file, 'script': script, 'speedup': speedup})

    # Create a DataFrame from the speed-up values
    speedup_df = pd.DataFrame(speedup_values)

    # Group by 'script' to get the overall average speed-up across all files
    overall_speedup = speedup_df.groupby('script')['speedup'].mean().reset_index()
    overall_speedup['file'] = 'Overall Average'  # Add a label for overall averages

    # Concatenate both DataFrames
    combined_df = pd.concat([speedup_df, overall_speedup], ignore_index=True)

    # Extract unique files and scripts
    unique_files = combined_df['file'].unique()
    unique_scripts = combined_df['script'].unique()

    # Set up the bar positions
    bar_width = 0.2  # Width of each bar
    x = np.arange(len(unique_files))  # X locations for the groups

    # Plotting
    plt.figure(figsize=(14, 8))

    for i, script in enumerate(unique_scripts):
        # Extract data for the current script
        script_data = combined_df[combined_df['script'] == script]

        # Get the speedup values in the order of unique_files
        values = [script_data[script_data['file'] == f]['speedup'].values[0] if f in script_data['file'].values else 0
                  for f in unique_files]

        # Plot bars for this script with a specific color
        plt.bar(x + i * bar_width, values, bar_width, label=script,
                color=colors.get(script, 'gray'))  # Default to 'gray' if script not in colors

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(x + bar_width, unique_files, rotation=45, ha="right")
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.30), ncol=len(unique_scripts))
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, filename))  # Save plot in the results directory
    plt.close()


# Generic function to plot grouped horizontal bar charts
def plot_grouped_horizontal_bar_chart(df, column, results_dir, colors, title, xlabel, filename):
    # Group by 'file' and 'script' to get the values for the specified column
    grouped = df.groupby(['file', 'script'])[column].mean().reset_index()

    # Extract unique files and scripts
    unique_files = grouped['file'].unique()
    unique_scripts = grouped['script'].unique()

    # Set up the bar positions
    bar_height = 0.2  # Height of each bar
    y = np.arange(len(unique_files))  # Y locations for the groups

    # Plotting
    plt.figure(figsize=(14, 8))

    for i, script in enumerate(unique_scripts):
        # Extract data for the current script
        script_data = grouped[grouped['script'] == script]

        # Get the column values in the order of unique_files
        values = [script_data[script_data['file'] == f][column].values[0] if f in script_data['file'].values else 0 for
                  f in unique_files]

        # Plot horizontal bars for this script with a specific color
        plt.barh(y + i * bar_height - (bar_height * (len(unique_scripts) - 1) / 2), values, bar_height, label=script,
                 color=colors.get(script, 'gray'))  # Default to 'gray' if script not in colors

    plt.title(title)
    plt.xlabel(xlabel)
    plt.yticks(y, unique_files, rotation=45)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=len(unique_scripts))
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, filename))  # Save plot in the results directory
    plt.close()

# Generic function to plot grouped horizontal bar charts with overall averages
def plot_grouped_horizontal_bar_chart_with_overall(df, column, results_dir, colors, title, xlabel, filename):
    # Group by 'file' and 'script' to get the values for the specified column
    grouped = df.groupby(['file', 'script'])[column].mean().reset_index()

    # Calculate overall average for each script
    overall_avg = grouped.groupby('script')[column].mean().reset_index()
    overall_avg['file'] = 'Overall Average'  # Add a label for overall averages

    # Concatenate both DataFrames
    combined_df = pd.concat([grouped, overall_avg], ignore_index=True)

    # Extract unique files and scripts
    unique_files = combined_df['file'].unique()
    unique_scripts = combined_df['script'].unique()

    # Set up the bar positions
    bar_height = 0.2  # Height of each bar
    y = np.arange(len(unique_files))  # Y locations for the groups

    # Plotting
    plt.figure(figsize=(14, 8))

    for i, script in enumerate(unique_scripts):
        # Extract data for the current script
        script_data = combined_df[combined_df['script'] == script]

        # Get the column values in the order of unique_files
        values = [script_data[script_data['file'] == f][column].values[0] if f in script_data['file'].values else 0 for
                  f in unique_files]

        # Plot horizontal bars for this script with a specific color
        plt.barh(y + i * bar_height - (bar_height * (len(unique_scripts) - 1) / 2), values, bar_height, label=script,
                 color=colors.get(script, 'gray'))  # Default to 'gray' if script not in colors

    plt.title(title)
    plt.xlabel(xlabel)
    plt.yticks(y, unique_files, rotation=45)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=len(unique_scripts))
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, filename))  # Save plot in the results directory
    plt.close()


# Main function to load data and call plotting functions
def plot_results(results_dir):

    # Load CSV files from the results directory
    memory_usage_df = pd.read_csv(os.path.join(results_dir, 'memory_usage.csv'))
    timings_df = pd.read_csv(os.path.join(results_dir, 'timings.csv'))
    quality_score_df = pd.read_csv(os.path.join(results_dir, 'quality_scores.csv'))

    # Convert peak memory and total allocated memory from bytes to MB
    memory_usage_df['peak_memory_MB'] = memory_usage_df['peak_memory'] / 1048576
    memory_usage_df['total_allocated_MB'] = memory_usage_df['total_allocated_bytes'] / 1048576

    # Round the avg_seconds column to 3 decimal places
    timings_df['avg_seconds'] = timings_df['avg_seconds'].round(3)

    # Merge dataframes on 'file' and 'script'
    merged_df = pd.merge(memory_usage_df, timings_df, on=['file', 'script'])
    merged_df = pd.merge(merged_df, quality_score_df, on=['file', 'script'])

    # Define colors for each script
    colors = {
        'run_unstructured': 'darkturquoise',  # Replace 'script1' with the actual script names
        'run_extractous_stream': 'black',  # Replace 'script2' with the actual script names
        'run_pypdf2': 'tab:orange'  # Replace 'script3' with the actual script names
    }

    # Execution times
    plot_grouped_bar_chart(merged_df, 'avg_seconds', results_dir, colors,
                           'Execution Times','Time (seconds)', 'execution_times.png')
    plot_grouped_horizontal_bar_chart(merged_df, 'avg_seconds', results_dir, colors,
                           'Execution Times', 'Time (seconds)', 'execution_times_hor.png')

    # Allocations
    plot_grouped_bar_chart(merged_df, 'total_allocated_MB', results_dir, colors,
                           'Total Allocated Memory', 'Memory (MB)', 'total_allocated_memory.png')
    plot_grouped_horizontal_bar_chart(merged_df, 'total_allocated_MB', results_dir, colors,
                           'Total Allocated Memory', 'Memory (MB)', 'total_allocated_memory_hor.png')

    # Peak memory
    plot_grouped_bar_chart(merged_df, 'peak_memory_MB', results_dir, colors,
                           'Peak RAM Memory Usage', 'Memory (MB)', 'peak_memory.png')

    plot_grouped_horizontal_bar_chart_with_overall(merged_df, 'peak_memory_MB', results_dir, colors,
                           'Peak RAM Memory Usage', 'Memory (MB)', 'peak_memory_hor.png')


    # Scores
    plot_grouped_bar_chart_with_overall(merged_df, 'score', results_dir, colors,
                           'Quality Scores', 'Score ', 'quality_scores.png')

    # Speed-up
    plot_grouped_bar_chart_speedup_with_overall(merged_df, 'avg_seconds', results_dir, colors,
                              'Speedup relative to run_unstructured', 'Speed-up (Higher is Better)',
                              'speedup_relative_to_unstructured.png', reference_script='run_unstructured')

    # Memory efficiency
    plot_grouped_bar_chart_speedup_with_overall(merged_df, 'total_allocated_MB', results_dir, colors,
                                                'Memory Allocations efficiency relative to run_unstructured', 'Memory Allocations Savings (Higher is Better)',
                                                'memory_efficiency_relative_to_unstructured.png',
                                                reference_script='run_unstructured')


# Entry point for the script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: '{sys.argv[0]}' <results_dir>")
        sys.exit(1)

    results_directory = sys.argv[1]
    if not os.path.isdir(results_directory):
        raise FileNotFoundError(f"Directory does not exist: '{results_directory}'")

    plot_results(results_directory)
