#pragma once

#include <string>
#include <vector>

struct SummaryRow {
    std::string team;
    long long total_points;
    int row_count;
};

std::vector<SummaryRow> summarize_csv(const std::string& csv);
