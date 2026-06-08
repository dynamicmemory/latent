#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <sstream>

using VecStr = std::vector<std::string>;

VecStr process_query(const std::string prompt);
VecStr split_words(const std::string &input);
VecStr match_records(const VecStr keywords);
std::string build_prompt(const std::string prompt, const VecStr records);
void query_model(const std::string input);
VecStr stopping_words();


int main(void) {

    while (true) {
        // Get user input
        std::string prompt;
        std::cout << "Enter Prompt >> ";
        std::getline(std::cin, prompt);

        if (prompt == "quit")
            break;
       
        // Process the prompt for keywords
        VecStr keywords = process_query(prompt);
         
        // Retrieve records containing keywords 
        VecStr records = match_records(keywords);

        // Build prompt 
        std::string input = build_prompt(prompt, records);

        // Send it to the model
        query_model(input);

    }
    return 0;
}

VecStr process_query(const std::string prompt) {
    std::transform(prompt.begin(), prompt.end(), prompt.begin(), 
            [](unsigned char c) { return std::tolower(c); });

    VecStr stop_words = stopping_words();
    VecStr prompt_vec = split_words(prompt);
    VecStr keywords;

    for (auto pword : prompt_vec) {
        bool in = false;

        for (auto sword : stop_words)
            if (pword == sword) 
                in = true;

        if (in) {
            in = false;
            continue;
        }
        keywords.push_back(pword);
    }

    return keywords;    
}

VecStr split_words(const std::string &input) {
    std::istringstream stream(input);
    VecStr output;
    std::string word;
    while (stream >> word) 
        output.push_back(word);
    return output;
}

VecStr match_records(const VecStr keywords) {

}

std::string build_prompt(const std::string prompt, const VecStr records) {

}

void query_model(const std::string input) {

}

VecStr stopping_words() {
    VecStr words = {"a","about","above","after","again","against","all",
        "am","an","and","any","are","as","at","be","because","been","before",
        "being","below","between","both","but","by","could","did","do","does",
        "doing","down","during","each","few","for","from","further","had","has",
        "have","having","he","her","here","hers","herself","him","himself","his",
        "how","i","if","in","into","is","it","its","itself","just","me","more",
        "most","my","myself","no","nor","not","now","of","off","on","once","only",
        "or","other","our","ours","ourselves","out","over","own","same","she","should",
        "so","some","such","than","that","the","their","theirs","them","themselves",
        "then","there","these","they","this","those","through","to","too","under",
        "until","up","very","was","we","were","what","when","where","which","while",
        "who","whom","why","will","with","you","your","yours","yourself","yourselves"};
    return words;
}
