
/*
Prompt is fed into a key word extractor
  - lowercase all words
  - splits all words 
  - remove stopping words 

Database is searched for matching content from key words extracted 
  - give each database entry a score for how many words match keywords
  - return top 5 to 10 

Prompt reconstructed using data from database 
  - build context from returned results (unsure how to do this yet) 
  - Prompt scaffolding {
      context:
        {retireved context}

      question:
        {original user prompt}
    }

Reponse displayed
  - Print tokens as they return.

*/

// Interfaces 
class Database {};
class Model {};


#include <iostream>
#include <string>
#include <vector>



int main(void) {

    // QueryProcessor qp = QueryProcessor("keyword"); // Perhaps different processing methods
    // Database db = Database("sqlite"); // sqlite would be arg[1] maybe
    // ContextBuilder cb = ContextBUilder();
    // Model m = Model("ollama");
    // PromptBuilder pb = PromptBuilder();

    while (true) {
        std::string prompt;

        std::cout << "Enter prompt >> ";
        std::getline(std::cin, prompt);

        // Process the users prompt
        std::vector<std::string> keywords = qp.process(prompt);

        // Retrieve records matching prompt keywords
        std::vector<std::string> records = db.retrieve(keywords);

        // Build context 
        std::string context = cb.build(records)

        prompt = pb.construct(prompt, context);
        m.query(prompt);
        
    }
    return 0;
};


