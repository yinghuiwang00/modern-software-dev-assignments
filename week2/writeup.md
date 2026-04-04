# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Write comprehensive unit tests for the `extract_action_items_llm()` function in `week2/app/services/extract.py`. The tests should be added to `week2/tests/test_extract.py`.

Requirements:
1. Mock the OpenAI/Zhipu API client to avoid actual API calls during testing
2. Use pytest as the testing framework (already configured in pyproject.toml)
3. Import the function: `from ..app.services.extract import extract_action_items_llm`

Test Cases to Cover:

1. **Bullet Lists Test** - Test extraction of bullet points with different formats:
   - Text containing "- [ ] Set up database"
   - Text containing "* implement API extract endpoint"
   - Text containing "1. Write tests"
   - Verify correct extraction of action items

2. **Keyword-Prefixed Lines Test** - Test extraction of lines with action keywords:
   - Text containing "todo: Review code"
   - Text containing "action: Fix bug"
   - Text containing "next: Deploy to production"
   - Verify correct extraction with keywords removed

3. **Empty Input Test** - Test handling of empty or whitespace-only input:
   - Empty string should return empty list
   - Whitespace-only string should return empty list

4. **JSON Array Parsing Test** - Test successful JSON array response from LLM:
   - Mock the API to return valid JSON: '["Action 1", "Action 2"]'
   - Verify correct parsing and return

5. **Fallback to Heuristic Test** - Test fallback when LLM returns invalid JSON:
   - Mock the API to return invalid JSON or plain text
   - Verify the function falls back to `extract_action_items()` heuristic extraction

6. **Markdown-wrapped JSON Test** - Test parsing of JSON wrapped in markdown code blocks:
   - Mock API to return: ```json\n["Action 1", "Action 2"]\n```
   - Verify correct parsing

7. **Mixed Content Test** - Test extraction from realistic meeting notes:
   - Bullet points
   - Action keywords
   - Narrative sentences mixed with action items

Make sure to:
- Use pytest's `unittest.mock` or `mocker` fixture for mocking
- Follow the existing test style in `test_extract.py`
- Include descriptive test names
- Add comments explaining what each test validates
- Ensure tests are isolated and don't depend on external services

``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```

### Exercise 2: Add Unit Tests
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
TODO
``` 

Generated/Modified Code Snippets:
```
TODO: List all modified code files with the relevant line numbers. (We anticipate there may be multiple scattered changes here – just produce as comprehensive of a list as you can.)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 