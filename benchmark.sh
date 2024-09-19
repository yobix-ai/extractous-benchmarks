#!/bin/bash

DO_BENCHMARK_SPEED=1
DO_PROFILE_MEMORY=1

WARMUP_RUNS=2 # Number of warmup runs (hyperfine handles this)
TIMED_RUNS=5 # Number of benchmarked runs to calculate average speed

# List of Python scripts to benchmark
SCRIPTS_SRC_DIR="src"
#SCRIPTS=("run_pypdfium2.py")
SCRIPTS=("run_extractous_stream.py" "run_unstructured.py" "run_pypdf2.py")

DATASET_FILES_DIR="dataset/sec10-filings"
DATASET_GT_DIR="dataset/sec10-ground-truth"
INPUT_FILES=(
 "2022_Q3_AAPL.pdf"  "2022_Q3_AMZN.pdf"  "2022_Q3_INTC.pdf"  "2022_Q3_MSFT.pdf"  "2022_Q3_NVDA.pdf"
 "2023_Q1_AAPL.pdf"  "2023_Q1_AMZN.pdf"  "2023_Q1_INTC.pdf"  "2023_Q1_MSFT.pdf"  "2023_Q1_NVDA.pdf"
# "2023_Q2_AAPL.pdf"  "2023_Q2_AMZN.pdf"  "2023_Q2_INTC.pdf"  "2023_Q2_MSFT.pdf"  "2023_Q2_NVDA.pdf"
# "2023_Q3_AAPL.pdf"  "2023_Q3_AMZN.pdf"  "2023_Q3_INTC.pdf" "2023_Q3_MSFT.pdf"  "2023_Q3_NVDA.pdf"
)

#DATASET_FILES_DIR="dataset/pypdf-files"
#DATASET_GT_DIR="dataset/pypdf-ground-truth"
#INPUT_FILES=(
#  "2201.00214.pdf"  "2201.00151.pdf"  "1707.09725.pdf"  "2201.00021.pdf"  "2201.00037.pdf"
#  "2201.00069.pdf"  "2201.00178.pdf"  "2201.00201.pdf"  "1602.06541.pdf"  "2201.00200.pdf"
#  "2201.00022.pdf"  "2201.00029.pdf"  "1601.03642.pdf"  "GeoTopo.pdf"
#)

RESULTS_TAG="$(basename "$DATASET_FILES_DIR")_$(date +"%d_%m_%Y")"
RESULTS_DIR="results/$RESULTS_TAG"
RESULTS_EXTRACT_OUT_DIR="$RESULTS_DIR/extract-output"
RESULTS_HYPERFINE_OUT_DIR="$RESULTS_DIR/hyperfine-output"
RESULTS_MEMRAY_BIN_DIR="$RESULTS_DIR/memray-profiles"

# make directories
mkdir -p "$RESULTS_EXTRACT_OUT_DIR" "$RESULTS_HYPERFINE_OUT_DIR" "$RESULTS_MEMRAY_BIN_DIR"

# Temp file for benchmark timings
TIMINGS_FILE="$RESULTS_DIR/timings.csv"
echo "file,script,avg_seconds" > "$TIMINGS_FILE"

# Memory profiling output file
QUALITY_SCORES_FILE="$RESULTS_DIR/quality_scores.csv"
echo "file,script,score"  > "$QUALITY_SCORES_FILE"

# Memory profiling output file
MEMORY_USAGE_FILE="$RESULTS_DIR/memory_usage.csv"
echo "file,script,total_allocated_bytes,total_allocations,peak_memory"  > "$MEMORY_USAGE_FILE"


print_experiment_info() {
    local dataset_directory="$1"
    local results_out_dir="$2"

    # Get processor name from /proc/cpuinfo
#    cpu_name=$(grep -m 1 'model name' /proc/cpuinfo | awk -F': ' '{print $2}' | \
#              sed -E 's/\(R\)/_/g' | sed 's/CPU//g' | sed 's/Core(TM)//g' | sed 's/@//g' | \
#              sed 's/ //g' | sed 's/ /_/g')

    cpu_model=$(grep -m 1 'model name' /proc/cpuinfo | awk -F': ' '{print $2}')
    total_ram=$(grep MemTotal /proc/meminfo | awk '{print int($2 / 1000 / 1000)}')
    curr_date=$(date --utc)
    os_details=$(uname -a)
    dataset_name=$(basename "$dataset_directory")
    # Combine into a tag

    echo "cpu_model: $cpu_model" > "$results_out_dir/info.txt"
    echo "total_ram: ${total_ram} GB" >> "$results_out_dir/info.txt"
    echo "dataset: $dataset_name" >> "$results_out_dir/info.txt"
    echo "os_details: $os_details" >> "$results_out_dir/info.txt"
    echo ""
    echo "timestamp: $curr_date" >> "$results_out_dir/info.txt"
}

# function used for naming output files
get_file_basename(){
  local input_file="$1"

  base_name=$(basename "$input_file")
  file_name_ext="${base_name//./_}"
  echo "$file_name_ext"
}

get_script_basename(){
  local script="$1"

  script_base_name="${script%.*}"
  echo "$script_base_name"
}



# Function for timing benchmarking using hyperfine
benchmark_speed() {
    local script="$1"
    local input_file="$2"
    local output_file="$3"

    script_basename=$(get_script_basename "$script")
    file_basename=$(get_file_basename "$input_file")
    qualifier_name="${file_basename}_${script_basename}"

    echo ""
    echo "Benchmarking speed of $qualifier_name using hyperfine..."

    # Run hyperfine with warmup and timed runs
    hyperfine_json="${RESULTS_HYPERFINE_OUT_DIR}/${qualifier_name}_timing.json"
    if [ "$DO_BENCHMARK_SPEED" == "1" ]; then
      hyperfine --warmup "$WARMUP_RUNS" --min-runs "$TIMED_RUNS" "python ${SCRIPTS_SRC_DIR}/${script} ${input_file} ${output_file}" --export-json "$hyperfine_json"
    fi
    # Extract the mean time from hyperfine JSON output
    avg_execution_time=$(jq '.results[0].mean' "$hyperfine_json")
    echo "Average execution time for $script with input $input_file: $avg_execution_time seconds"

    # Save the timing result
    echo "$file_basename,$script_basename,$avg_execution_time" >> $TIMINGS_FILE
}

benchmark_quality() {
    local script="$1"
    local input_file="$2"
    local output_file="$3"
    local ground_truth_file="$4"

    script_basename=$(get_script_basename "$script")
    file_basename=$(get_file_basename "$input_file")
    qualifier_name="${file_basename}_${script_basename}"

    echo ""
    echo "Calculating similarity score for $qualifier_name ..."

    score=$(python "${SCRIPTS_SRC_DIR}/calc_similarity_score.py" "$output_file" "$ground_truth_file")
    echo "Similarity score for $qualifier_name: $score "

    # Save the timing result
    echo "$file_basename,$script_basename,$score" >> $QUALITY_SCORES_FILE
}

# Function for memory profiling using memray
profile_memory() {
    local script="$1"
    local input_file="$2"
    local output_file="$3"

    script_basename=$(get_script_basename "$script")
    file_basename=$(get_file_basename "$input_file")
    qualifier_name="${file_basename}_${script_basename}"

    echo ""
    echo "Profiling memory usage of $qualifier_name using memray..."

    # Generate bin file
    MEMRAY_BIN_FILE="$RESULTS_MEMRAY_BIN_DIR/${qualifier_name}.bin"
    MEMRAY_JSON_REPORT="${MEMRAY_BIN_FILE%.bin}_stats.json"

    if [ "$DO_PROFILE_MEMORY" == "1" ]; then
      #python -m memray run --native --force -o "$MEMRAY_BIN_FILE" "./$script" "$input_file" "$output_file"
      python -m memray run --force -o "$MEMRAY_BIN_FILE" "${SCRIPTS_SRC_DIR}/${script}" "$input_file" "$output_file"

      # Generate memray flamegraph
      python -m memray flamegraph --force "$MEMRAY_BIN_FILE"

      # Generate memray stats report
      python -m memray stats --force --json --output "$MEMRAY_JSON_REPORT" "$MEMRAY_BIN_FILE"
    fi

    # Extract total memory allocated from the JSON report
    TOTAL_BYTES_ALLOCATED=$(jq '.total_bytes_allocated' "$MEMRAY_JSON_REPORT")
    TOTAL_ALLOCATIONS=$(jq '.total_num_allocations' "$MEMRAY_JSON_REPORT")
    MEMORY_PEAK_BYTES=$(jq '.metadata.peak_memory' "$MEMRAY_JSON_REPORT")
    #STATS_TOTAL_ALLOCATIONS=$(jq '.metadata.total_allocations' "$MEMRAY_JSON_REPORT")
    echo "Total memory allocated by $qualifier_name: $TOTAL_BYTES_ALLOCATED bytes, $TOTAL_ALLOCATIONS allocations"

    # Save the memory usage result
    echo "$file_basename,$script_basename,$TOTAL_BYTES_ALLOCATED,$TOTAL_ALLOCATIONS,$MEMORY_PEAK_BYTES" >> $MEMORY_USAGE_FILE
}

# Print experiment info
print_experiment_info "$DATASET_FILES_DIR" "$RESULTS_DIR"

# Main loop to process each script with each input file
for script in "${SCRIPTS[@]}"; do
    for input_file in "${INPUT_FILES[@]}"; do
        # Define the full path for the file
        file_path="${DATASET_FILES_DIR}/${input_file}"

        # Define the ground truth file
        name_no_ext="${input_file%.*}"
        ground_truth_file="${DATASET_GT_DIR}/${name_no_ext}.txt"

        # Define the output file path for this run
        qualifier_name="$(get_script_basename "$script")_$(get_file_basename "$input_file")"

        output_file="$RESULTS_EXTRACT_OUT_DIR/${qualifier_name}_output.txt"

        # Call the speed benchmarking function
        benchmark_speed "$script" "$file_path" "$output_file"

        benchmark_quality "$script" "$file_path" "$output_file" "$ground_truth_file"

        # Call the memory profiling function
        profile_memory "$script" "$file_path" "$output_file"


    done
done

echo "Benchmarking and profiling completed!"
echo ""
echo "You can plot the results using this command:"
echo "./plot_results.py $RESULTS_DIR"
