#!/bin/bash

function print_error {
    echo -e "\033[0;31m$1\033[0m"
}

function assert_equal {
    local expected_value="$1"
    local actual_value="$2"

    if [[ "$actual_value" == "$expected_value" ]]; then
        echo "Success: $actual_value"
    else
        print_error "Failure: Actual value '$actual_value' does not match expected value '$expected_value'."
        exit 1
    fi
}