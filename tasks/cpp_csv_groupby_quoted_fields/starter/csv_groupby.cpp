#include "csv_groupby.h"

#include <algorithm>
#include <map>
#include <sstream>
#include <string>
#include <vector>

namespace {

std::vector<std::string> split_csv_line(const std::string& line) {
    std::vector<std::string> fields;
    std::string field;
    bool in_quotes = false;
    size_t i = 0;
    size_t len = line.size();

    while (i <= len) {
        if (i == len) {
            // End of line — push whatever we have
            fields.push_back(field);
            break;
        }

        char c = line[i];

        if (in_quotes) {
            if (c == '"') {
                // Check for escaped quote ""
                if (i + 1 < len && line[i + 1] == '"') {
                    field += '"';
                    i += 2;
                } else {
                    // End of quoted field
                    in_quotes = false;
                    i++;
                }
            } else {
                field += c;
                i++;
            }
        } else {
            if (c == '"') {
                in_quotes = true;
                i++;
            } else if (c == ',') {
                fields.push_back(field);
                field.clear();
                i++;
            } else {
                field += c;
                i++;
            }
        }
    }

    return fields;
}

}  // namespace

std::vector<SummaryRow> summarize_csv(const std::string& csv) {
    std::stringstream stream(csv);
    std::string line;
    bool first_line = true;
    std::map<std::string, SummaryRow> grouped;

    while (std::getline(stream, line)) {
        // Strip \r for CRLF input
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        if (line.empty()) {
            continue;
        }
        if (first_line) {
            first_line = false;
            continue;
        }

        const auto fields = split_csv_line(line);
        if (fields.size() < 3) {
            continue;
        }

        auto& row = grouped[fields[0]];
        row.team = fields[0];
        row.total_points += std::stoll(fields[2]);
        row.row_count += 1;
    }

    std::vector<SummaryRow> result;
    for (const auto& [_, row] : grouped) {
        result.push_back(row);
    }

    // Sort by total_points descending, then team ascending
    std::sort(
        result.begin(),
        result.end(),
        [](const SummaryRow& left, const SummaryRow& right) {
            if (left.total_points != right.total_points) {
                return left.total_points > right.total_points;
            }
            return left.team < right.team;
        }
    );
    return result;
}
