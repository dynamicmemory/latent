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
    std::vector<std::string> context;
};

// Utilities.h 
std::vector<std::string> split_string(const std::string &input);
std::string normalise(std::string &input);

// Utilities.cpp
/* Utility function for splitting strings into string vectors*/
std::vector<std::string> split_string(const std::string &input) {
    std::istringstream stream(input);
    std::vector<std::string> output;
    std::string word;
    while (stream >> word) 
        output.push_back(word);
    return output;
}

std::string normalise(std::string &input) {
    // drop all chars to lowercase
    std::transform(input.begin(), input.end(), input.begin(), 
            [](unsigned char c) { return std::tolower(c); });

    // drop all puncuation
    std::replace_if(input.begin(), input.end(), 
            [](unsigned char c) { return std::ispunct(c); }, ' ');
    return input;
}


// QueryAnalyser.h
class QueryAnalyser {
private:
    std::vector<std::string> stop_words;
public:
    QueryAnalyser() { stop_words = stopping_words(); }
    std::vector<std::string> analyse(std::string prompt);
    std::vector<std::string> stopping_words();
};

// QueryAnalyser.cpp
std::vector<std::string> QueryAnalyser::analyse(std::string prompt) {
    prompt = normalise(prompt);

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

/* Hard coded set of stopping words*/
std::vector<std::string> QueryAnalyser::stopping_words() {
    std::string line;
    std::vector<std::string> words;
    std::ifstream file("./stopping_words.txt");

    while (std::getline(file, line)) {
        words.push_back(line);
    }
    return words;
}


// KnowledgeBase.h
/* TODO: Support a directory full of .txt, .db, .pdf, etc files to read knowledge from */
class KnowledgeBase {
private:
    std::vector<std::string> records;
public:
    KnowledgeBase(/*TODO: PASS IN THE KNOWLEDGEBASE?*/) { 
        records = load_knowledge(); 
    }
    std::vector<std::string> get_knowledge() { return records; }
    std::vector<std::string> load_knowledge();
};


// KnowledgeBase.cpp
/* Hard coded set of knowledge
 * TODO: KnowledgeBase wont always be a txt file, add support or turn into interface
 */
std::vector<std::string> KnowledgeBase::load_knowledge() {
    std::string line;
    std::vector<std::string> knowledge;
    std::ifstream file("./knowledge_base.txt"); // TODO: Change to passed in kb

    // TODO: Handle failure
    if (!file) {
        std::cerr << "Failed to open file\n";
    }

    while (std::getline(file, line)) {
        // drop all puncuation
        std::replace_if(line.begin(), line.end(), 
                [](unsigned char c) { return std::ispunct(c); }, ' ');

        knowledge.push_back(line);
    }
    return knowledge;
}


// RetrivalEngine.h
/* Retrieves matching records from the knowledge base related to the users prompt */
class RetrivalEngine {
private:
public:
    std::vector<std::string> retrieve_context(std::vector<std::string> keywords,
                                              std::vector<std::string> records);
    std::vector<std::string> sort_context(std::vector<std::string> context);
};

// RetrivalEngine.cpp
std::vector<std::string> RetrivalEngine::retrieve_context(
        std::vector<std::string> keywords, std::vector<std::string> records) {

    struct Match { std::string record; int score = 0; };

    std::vector<Match> matches;
    std::vector<std::string> context;

    for (auto rec : records) {
        Match m;
        // Process each record, lower case them, strip puncuation 
        rec = normalise(rec);
        std::vector<std::string> record_keywords = split_string(rec);

        m.record = rec;
        // TODO int score_record(keywords, record_keywords) return score into m.score
        for (auto word : keywords) {
            for (auto recword : record_keywords) 
                if (word == recword)
                    m.score++;
        }

        if (m.score > 0)
            matches.push_back(m);
    }

    std::sort(matches.begin(), matches.end(), 
        [](const Match &a, const Match &b) { return a.score > b.score;});

    // Take the 5 best matched records
    for (auto match : matches)
        if (context.size() < 5) {
            context.push_back(match.record);
            std::cout << "Record: " << match.record << " Score: " << match.score << "\n";
        }
    return context;
}


// ContextBuilder.h
class ContextBuilder {
    private: 
    public:
        std::string build(std::string prompt, std::vector<std::string> context);
};

// ContextBuilder.cpp
std::string ContextBuilder::build(std::string prompt, std::vector<std::string> context) {
    std::string output = "context: "; 
    for (auto con : context)
        output += con + " ";
    output += " question: " + prompt;
    return output;
}

// ModelRuntime.h
class ModelRuntime {
private:
public:
    void query(std::string prompt);
};

// ModelRuntime.cpp
void ModelRuntime::query(std::string prompt) {

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


// Agent.h
class Agent {
    private:
    public:
        QueryAnalyser analyser;
        RetrivalEngine retriever;
        KnowledgeBase kb;
        ContextBuilder builder; 
        ModelRuntime model;

        void ask(Query query);
};

// Agent.cpp
void Agent::ask(Query query) {
    query.keywords = analyser.analyse(query.prompt);
    auto records = kb.get_knowledge();
    query.context = retriever.retrieve_context(query.keywords, records);
    auto reconstructed = builder.build(query.prompt, query.context);
    model.query(reconstructed);
}

// main.cpp
int main(void) {

    Agent smith = Agent();

    while (true) {
        // Get user input
        Query q;
        std::string prompt; 
        std::cout << "Enter Prompt >> ";
        std::getline(std::cin, q.prompt);

        if (q.prompt == "quit")
            break;

        smith.ask(q);
    }
    return 0;
}
