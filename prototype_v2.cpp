#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <sstream>
#include <netdb.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cstring>
#include <fstream>
#include <sstream>

struct Query {
    std::string prompt;
    std::vector<std::string> keywords;
};


class QueryAnalyser {
private:
public: 
    std::vector<std::string> analyse(std::string prompt) {
        std::transform(prompt.begin(), prompt.end(), prompt.begin(), 
                [](unsigned char c) { return std::tolower(c); });

        std::vector<std::string> stop_words = stopping_words();
        std::vector<std::string> prompt_vec = split_string(prompt);
        std::vector<std::string> keywords;

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

    /* Utility function for splitting strings into string vectors*/
    std::vector<std::string> split_string(const std::string &input) {
        std::istringstream stream(input);
        std::vector<std::string> output;
        std::string word;
        while (stream >> word) 
            output.push_back(word);
        return output;
    }

    /* Hard coded set of stopping words*/
    std::vector<std::string> stopping_words() {
        std::vector<std::string> words = {"a","about","above","after","again","against","all",
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
};


class KnowledgeBase {
private:
    std::vector<std::string> records;
public:
    KnowledgeBase(/*TODO: PASS IN THE KNOWLEDGEBASE?*/) { 
        records = load_knowledge(); 
    }

    std::vector<std::string> get_knowledge() { return records; }

    /* Hard coded set of knowledge
     * TODO: KnowledgeBase wont always be a txt file, add support or turn into interface
     */
    std::vector<std::string> load_knowledge() {
        std::string line;
        std::vector<std::string> knowledge;
        std::ifstream file("./knowledge_base.txt"); // TODO: Change to passed in kb
        
        // TODO: Handle failure
        if (!file) {
            std::cerr << "Failed to open file\n";
        }

        while (std::getline(file, line)) {
            knowledge.push_back(line);
        }
        return knowledge;
    }
};


/* Retrieves matching records from the knowledge base related to the users prompt */
class RetrivalEngine {
private:
public:
    std::vector<std::string> retrieve_context(std::vector<std::string> keywords,
                                              std::vector<std::string> records) {
        std::vector<std::string> context;

        for (auto rec : records) {
            // Process each record, lower case them, strip stopping words
            std::transform(rec.begin(), rec.end(), rec.begin(), 
                [](unsigned char c) { return std::tolower(c); });
            std::vector<std::string> record_keywords = split_string(rec);

            for (auto word : keywords) { 
                bool in = false;
                // For each word in the keywords from the current record 
                for (auto recword : record_keywords) 
                    // If one word matches, then add the whole untouched record
                    if (word == recword) {
                        context.push_back(rec);
                        in = true;                
                        break;
                    }
                // Stops looking at record if a match has already occured
                if (in)
                    break;
            }
        }
        return context;
    }

    /* Utility function for splitting strings into string vectors*/
    std::vector<std::string> split_string(const std::string &input) {
        std::istringstream stream(input);
        std::vector<std::string> output;
        std::string word;
        while (stream >> word) 
            output.push_back(word);
        return output;
    }
};


class ContextBuilder {
private: 
public:
    std::string build(std::string prompt, std::vector<std::string> context) {
        std::string output = "context: "; 
        for (auto con : context)
            output += con + " ";
        output += " question: " + prompt;
        return output;
    }
};


class ModelRuntime {
private:
public:
    void query(std::string prompt) {

        const char host[] = "127.0.0.1";
        const char port[] = "11434";

        struct addrinfo hints, *addr;
        ::memset(&hints, 0, sizeof(addrinfo));
        hints.ai_socktype = SOCK_STREAM;
        hints.ai_family = AF_UNSPEC;

        int status = ::getaddrinfo(host, port, &hints, &addr);
        if (status != 0) {
            std::cout << "getaddrinfo failed\n";
            return;
        }

        int server = ::socket(addr->ai_family, addr->ai_socktype, addr->ai_protocol);
        if (server < 0) {
            std::cout << "socket failed\n";
            return;
        }

        int connect = ::connect(server, addr->ai_addr, addr->ai_addrlen);
        if (connect < 0) {
            std::cout << "connect failed\n";
            return;
        }
        ::freeaddrinfo(addr);

        std::string body = 
            "{\"model\": \"llama3.1:8B\","
            // "{\"model\": \"qwen3:8B\","
            "\"prompt\": \"" + prompt + "\","
            "\"stream\": true,"
            "\"think\": false}";

        std::string http_req = 
            "POST /api/generate HTTP/1.1\r\n"
            "Host: localhost:11434\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: " + std::to_string(body.size()) + "\r\n"
            "\r\n" + 
            body;

        std::cout << prompt;

        ssize_t send = ::send(server, http_req.c_str(), http_req.size(), 0);
        std::cout << "Size sent: " << send << "\n";

        while (1) {

            // std::cout << "in the while loop\n";
            char res[4096];
            char *p;
            int recieve = ::recv(server, res, sizeof(res), 0);

            // std::cout << res ;
            if (recieve <=0) {
                std::cout << "Connection closed or stalled \n";
                break;
            }

            // Find the response and print it to the terminal char by char
            if ((p=strstr(res, "\"response\":\""))) {
                p+=12;

                while (*p && *p != '"')
                    putchar(*p++);
            }

            fflush(stdout);
            // Exit loop on response finished
            if ((p=strstr(res, "\"done\":true"))) {
                printf("\n");
                break;
            }
        }
    }
};


class Agent {
private:
public:
    QueryAnalyser analyser;
    RetrivalEngine retriever;
    KnowledgeBase kb;
    ContextBuilder builder; 
    ModelRuntime model;

    void ask(std::string prompt) {
        auto keywords = analyser.analyse(prompt);
        auto records = kb.get_knowledge();
        auto context = retriever.retrieve_context(keywords, records);
        auto reconstructed = builder.build(prompt, context);
        model.query(reconstructed);
    }
};

int main(void) {

    Agent smith = Agent();

    while (true) {
        // Get user input
        std::string prompt; 
        std::cout << "Enter Prompt >> ";
        std::getline(std::cin, prompt);

        if (prompt == "quit")
            break;

        smith.ask(prompt);
    }
    return 0;
}
