# Multiple Language Support MCP

**User:** Ohad Rubin (ohadr@mail.tau.ac.il)  
**Created:** 6/25/2025 19:57  
**Updated:** 6/26/2025 6:46  
**Exported:** 6/26/2025 9:43  

## Prompt:
research what kind of changes are needed in order to allow multiple languages in OhadRubin/python-outline-mcp
i'm interested in these languages in the following order
- javascript
- typescript
- C++
- C

## Response:
To help you better, could you clarify what level of support you are looking for regarding multiple languages in the OhadRubin/python-outline-mcp repository? For example:

*   Are you looking to add parsing and outline generation for these languages?
    
*   Should the existing UI or output format change to accommodate multiple languages?
    
*   Do you expect language-specific plugins or a unified system?
    

Understanding your goals will help tailor the research effectively.

## Prompt:
"Are you looking to add parsing and outline generation for these languages?" yes

## Response:
Thanks for confirming. I’ll look into the changes needed in the OhadRubin/python-outline-mcp project to support parsing and outline generation for JavaScript, TypeScript, C++, and C, in that priority order.  
I’ll let you know once I’ve gathered the relevant findings.

Research completed in 7m · 12 sources · 36 searches

Support for Multiple Language Parsing in python-outline-mcp

Extending the Outline Generator to Multiple Languages
=====================================================

Current Architecture of the Outline Generator
---------------------------------------------

The **Python Outline MCP Tool** is currently a single-language parser centered on Python code. Its core is implemented in a single script (`outline.py`) which uses the `ast-grep` library to parse source code into an abstract syntax tree (AST) and extract an outline of functions and classes. The workflow is as follows:

*   **Parsing with ast-grep:** The tool reads the file content and creates an AST root via `SgRoot(content, "python")`[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). The second argument specifies the language grammar (in this case, `"python"`), indicating that the parser is configured for Python syntax. Internally, ast-grep uses language-specific tree-sitter grammars to build the AST (it supports many languages via built-in grammars[ast-grep.github.io](https://ast-grep.github.io/#:~:text=Polyglot)).
    
*   **AST Pattern Matching:** Once the AST is built, the tool queries it using structural patterns. It finds all function definitions and class definitions by matching Python code patterns. For example, it searches for patterns like `"def $FUNC($$$): $$$"` (function definitions without return annotations) and `"def $FUNC($$$) -> $$$: $$$"` (functions with return type annotations)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). Similarly, class definitions are found with patterns for classes with no base class (`"class $CLASS: $$$"`) and with base classes (`"class $CLASS($$$): $$$"`)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). These pattern strings leverage ast-grep’s syntax-aware matching to capture the name of the function or class into placeholders like `$FUNC` or `$CLASS`.
    
*   **Outline Construction:** The matches returned by `find_all` are AST nodes that contain information like the name and source code range. The tool then filters and formats these into an outline. In Python’s case, it separates _top-level functions_ from _methods defined inside classes_. This is done by iterating through all function nodes and excluding any whose start line lies within the range of a class node (thus filtering out class methods)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). Next, it appends each top-level function to the outline (prefixed with a gear icon `⚙️` and labeled as `def` with its line range)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). Then for each class, it adds an entry (prefixed with a courthouse icon `🏛️` labeled `class`) along with its line span[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py), and indents each method under that class (with a wrench icon `🔧` and `def` label)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). The result is a hierarchical list of definitions with line numbers, as shown in the README’s example output.
    
*   **File and Directory Handling:** The tool can operate on a single file or recursively on a directory. When given a directory, it searches for Python files (`*.py`). If the directory is a git repository, it uses `git ls-files` to list tracked `.py` files (respecting `.gitignore`), otherwise it falls back to a filesystem glob search[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). This logic is currently hard-coded for Python files. Each file’s outline is generated and concatenated, preceded by a file header line (`📁 filename`) and a separator line[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py).
    
*   **MCP Server Integration:** The script runs as an MCP (Model Context Protocol) server. There is a single tool function exposed, `python_outline(path, recursive=True, ...)`, which wraps the above logic[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). The MCP server is initialized with a descriptive name “Python Outline Generator 🐍”[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). In its current form, the tool name and documentation explicitly mention Python-only usage (e.g. _“Path to a Python file or directory”_ in the docstring)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py).
    

Overall, the existing architecture is **simple but Python-specific**. The parsing and outline generation rely on ast-grep’s Python AST, and the entire pipeline (file discovery, AST patterns, output formatting) assumes the input is Python code.

Language-Specific Implementation in the Current Tool
----------------------------------------------------

At present, the tool’s **language support is hard-coded for Python**. Key aspects of the language-specific implementation include:

*   **Parser Configuration:** The ast-grep parser is invoked with the language set to `"python"`[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). This tells ast-grep to use the Python grammar. No other languages are referenced in the code, so the parser configuration is effectively fixed. There is no conditional logic to select a different grammar or parser at runtime.
    
*   **AST Query Patterns:** The search patterns are written in Python’s syntax. For example:
    
    *   Function definitions are identified by the literal keyword `def` in the pattern[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). The pattern structure (`def $FUNC(...) -> ...: ...`) mirrors Python’s syntax for function declarations. This would **not match** equivalent constructs in other languages (e.g. JavaScript’s `function` or C++’s return type syntax) because those use different keywords/structures.
        
    *   Class definitions use the `class` keyword in patterns[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py), which again is specific to Python’s syntax (Python uses `class ClassName:` whereas, for instance, C++ uses `class ClassName { ... };` and JavaScript uses `class ClassName { ... }`).
        
    *   The inclusion of patterns both with and without `-> $$$` illustrates handling a Python-specific feature: optional return type annotations. The current implementation explicitly accounts for Python’s `-> type` syntax by providing an alternate pattern[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). This is a purely language-specific concern – other languages will have their own nuances (for example, C++ has return types before the function name, TypeScript has type annotations after parameters, etc.).
        
*   **Outline Formatting:** The output uses the Python keywords `def` and `class` literally in the text (alongside icons). This makes sense for Python code, but for other languages these labels might be inconsistent. (For instance, JavaScript functions are declared with the `function` keyword or as arrow functions, and C/C++ functions have no `def` keyword). Currently, the tool does not abstract these labels; they are part of the format string for Python outline entries[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). Moreover, the filtering logic for top-level functions assumes that only classes are “containers” for functions – it does not check for nested functions within other functions. In Python, functions can be defined inside other functions, and the current implementation would mistakenly treat those inner functions as top-level (since it only excludes functions inside classes). This is another Python-centric design choice that will need rethinking for languages like JavaScript, which frequently contain nested functions.
    

In summary, **all language-specific behavior is embedded directly in the code**: the parser is locked to Python’s AST, the search patterns are written in Python syntax, and even the output strings use Python keywords. There is no modular separation for different languages – the tool was clearly initially designed to handle Python only.

Changes Needed for Multi-Language Support
-----------------------------------------

To support JavaScript, TypeScript, C++, and C, the tool’s architecture must be made more flexible and modular. The following changes are needed:

*   **Parameterize the Language Selection:** Currently, the code always passes `"python"` to the AST constructor[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). We need to allow other languages to be specified. This could be done by adding a parameter (e.g. `language="python"`) to the outline function, or by providing separate functions for each language. For example, one approach is to generalize `python_outline` into a more generic `code_outline(path, language, ...)` that dispatches to the appropriate parser. Alternatively, we could register new MCP tool functions like `js_outline`, `cpp_outline`, etc., each internally calling a common outline generator with a different language setting. In either case, the ast-grep invocation should use the appropriate language code (e.g. `"javascript"`, `"typescript"`, `"cpp"`, `"c"`, etc.) as supported by ast-grep’s language list[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=Language%20Name%20Alias%20File%20Extension,exs)[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=Java%20,rs).
    
*   **Abstract Syntax Patterns per Language:** The pattern strings for finding functions and classes must be adapted for each target language’s syntax. The code should be refactored so that these patterns are not hard-coded for Python. Possible solutions include:
    
    *   Defining a dictionary or configuration structure that maps a language to its pattern set (e.g. `patterns["python"] = {...}`, `patterns["javascript"] = {...}`, etc.). Each entry would contain the patterns needed to identify top-level functions, classes, and class methods for that language.
        
    *   Implementing separate outline-generation routines for each language that encapsulate their syntax details. For instance, a `PythonOutlineGenerator` (using the existing logic) and new classes or functions `JavaScriptOutlineGenerator`, `CppOutlineGenerator`, etc. Each would define how to find functions and classes in that language’s AST. These could share a common interface so that the main workflow (reading files, iterating nodes, formatting output) remains largely the same.
        
    
    For languages in question:
    
    *   **JavaScript/TypeScript:** We would search for `function` declarations (e.g. pattern like `"function $FUNC($$$) { $$$ }"` for traditional functions) and `class` declarations (e.g. `"class $CLASS $$$ { $$$ }"` – accounting for optional `extends` clause). We should also consider arrow functions or function expressions assigned to variables at the top level. A decision needs to be made whether to include those in the outline. If yes, additional patterns such as `"$VAR = ($$$) => $$$"` might be needed to catch arrow functions assigned to identifiers. (Initially, focusing on named function declarations and classes might suffice.)
        
    *   **C++:** We need to find free function definitions and class/struct definitions. Patterns might look like `"$RET $FUNC($$$) { $$$ }"` to match function definitions (where `$RET` captures the return type segment, and `$FUNC` the name). Because C++ syntax is complex (functions may have return types that are multiple tokens, templates, etc.), multiple patterns or a more robust approach might be required. Class definitions can be matched with patterns like `"class $CLASS { $$$ };"` and `"struct $CLASS { $$$ };"` to include both keywords. We must ensure we only capture function _definitions_ (with bodies) and not forward declarations or pure virtual prototypes (which have no body and end with `;`). Using the presence of `{ $$$ }` in the pattern ensures we match only definitions with a body. One tricky aspect is C++ class methods defined outside the class, e.g. `ReturnType ClassName::Method(...) { ... }`. Those would appear as free function definitions in the AST (with qualified names). A robust implementation might detect the `ClassName::Method` pattern and group such functions under the corresponding class in the outline. This likely requires additional logic: the AST node or text will include `ClassName::Method` as the function name, so we could parse the qualifier and attach the method to the class’s section.
        
    *   **C:** We look for top-level function definitions in .c files. Since C has no classes, our outline for C would consist only of functions (and perhaps `struct` definitions if desired, though typically outlines focus on code routines). The pattern for functions could be similar to C++ (e.g. `"$RET $FUNC($$$) { $$$ }"`). We should also handle the special case of C’s _function prototypes_ (declarations without a body). As with C++, limiting the pattern to those with `{ ... }` will exclude prototypes. If needed, we could include `struct $NAME { $$$ };` patterns to list struct definitions, but this might be outside the scope of "functions and classes" and could be optional.
        
*   **Refactor File Handling:** The directory scanning logic must be generalized to handle different file extensions. Currently it looks for `*.py` files[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). We may introduce a mapping from language to file extensions (for example, JavaScript -> `[".js", ".jsx"]`, TypeScript -> `[".ts", ".tsx"]`, C++ -> `[".cpp", ".hpp", ".cxx", etc.]`, C -> `[".c", ".h"]`). Ast-grep already maintains a list of default extensions for each language[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=Language%20Name%20Alias%20File%20Extension,exs)[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=Java%20,rs); we can leverage that by either using its auto-detection (it can guess language by file extension) or by explicitly filtering files ourselves. If we continue to use git to list files, we’d adjust the `git ls-files` command to the appropriate pattern (e.g. `*.js` for JavaScript, `*.cpp` for C++, etc., possibly using multiple patterns if needed). For recursive filesystem search, we’d use the extension list per language in the glob (e.g. `rglob("*.js")` plus `*.jsx` for JS, etc.).
    
*   **Dynamic Output Labels:** We might want to adjust the output text to be more language-agnostic or language-aware. The current output lines include the keyword `def` for functions and `class` for classes. For consistency, we could continue to use these as symbols indicating a function or class regardless of language (they are preceded by icons which already differentiate function vs class). However, it may be clearer to use each language’s actual keyword for function definitions:
    
    *   For JavaScript/TypeScript, use `function` in the output (or simply omit the keyword and just list the name with an icon, since JS functions might also include constructors, etc.).
        
    *   For C/C++, perhaps just list the function name with the icon (since there’s no `def` keyword at all). For example, output “⚙️ **funcName** (line-range)” could suffice. Or we might prefix with the return type in C/C++ outlines for clarity. The design choice here should be consistent: either keep a generic marker like `def` for all languages or tailor the label to each language.
        
*   **Shared Logic vs. Custom Logic:** Identify which parts of the pipeline can remain common and which need specialization:
    
    *   Reading files, iterating through AST nodes, and formatting with line numbers are general and can be reused.
        
    *   The differences lie in how we _find_ the relevant AST nodes (patterns or queries) and how we _categorize_ them (e.g. what constitutes a “method” vs “top-level” in each language). We should structure the code such that the language-specific queries (and any filtering rules) are isolated. For instance, a common function could retrieve all “outline items” from the AST given a set of language patterns and perhaps post-filters.
        
    *   We may also need slight differences in filtering: For Python, we filtered out functions inside classes. For JavaScript, we’ll similarly filter out functions that are methods of classes (which in AST will appear inside class nodes) from the top-level list. But we might also consider filtering out functions defined inside other functions or inside methods (i.e., only list truly top-level functions). A robust approach could be to check the parent chain of a function node: if any ancestor is a class or another function, we exclude it from top-level. Implementing this check generally would cover all languages (this is an improvement even for Python to exclude nested inner defs). Ast-grep’s API allows traversing parent relationships or at least comparing ranges as done in Python; we can extend that logic accordingly.
        
*   **MCP Interface Changes:** With multiple languages supported, the MCP server might expose either one generalized endpoint or one per language. If a single `code_outline` tool is used, it should accept a `language` parameter (and perhaps default it based on file extension if not provided). If separate endpoints are used (one for each language), then the client or user would invoke different tools for each language. In either case, the user documentation (help text) should be updated to reflect multi-language usage instead of being Python-specific[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py). The server’s display name “Python Outline Generator 🐍” would also be updated to something like “Code Outline Generator” since it’s no longer Python-only.
    

In summary, **the code needs to be refactored for configurability**: the parser initialization, file selection, pattern matching, and output formatting should all depend on the specified language, rather than being fixed. This likely entails introducing a layer of abstraction (via configuration or polymorphic classes) for language-specific details, while keeping the overall outline generation process consistent.

Parsing Libraries and Tools for Each Target Language
----------------------------------------------------

To implement support for JavaScript, TypeScript, C++, and C, we should choose appropriate parsing tools or libraries for each. The good news is that the existing choice, **ast-grep**, is a polyglot tool that already supports all these languages out-of-the-box. Ast-grep’s underlying engine uses tree-sitter grammars for many languages and already lists support for JavaScript, TypeScript, C, C++, and more[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=,hs)[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=Java%20,rs). We can therefore continue to use ast-grep as a unified solution, simply by specifying the language. For completeness, here are suggestions for each language (including ast-grep and alternative tools):

*   **JavaScript:** Using ast-grep with the `"javascript"` language setting is likely the easiest route, as it leverages a robust tree-sitter JavaScript parser. We just need to supply JavaScript-specific patterns to find function and class declarations. Ast-grep’s pattern syntax will allow us to match JS constructs (e.g., `function` keyword, or class methods which in JS AST are identified differently than Python). If ast-grep is used, no additional external dependency is needed beyond what’s already in place. As alternatives, one could consider:
    
    *   _Tree-sitter directly:_ The tree-sitter project provides a Python binding and supports JavaScript grammar[stackoverflow.com](https://stackoverflow.com/questions/65076264/python-library-for-parsing-code-of-any-language-into-an-ast#:~:text=The%20library%20tree,binding%2C%20tons%20of%20language%20parsers). We could embed tree-sitter parsing directly and then traverse the parse tree to find functions and classes. This is essentially what ast-grep abstracts for us.
        
    *   _Esprima (JavaScript parser) port:_ Projects like **esprima-python** provide a JavaScript parser in Python[reddit.com](https://www.reddit.com/r/webscraping/comments/uuleeh/how_do_you_parse_a_javascript_script_with_python/#:~:text=How%20do%20you%20parse%20a,python.%20Upvote%203.%20Downvote). Esprima is a well-known JS parser (originally in JavaScript, but a Python port exists). Using it, we would have to manually walk the AST to collect function definitions (nodes of type FunctionDeclaration) and class definitions (ClassDeclaration and possibly FunctionExpression for named function expressions). This is doable but more manual work compared to ast-grep’s pattern matching.
        
    *   _ANTLR grammar:_ There are ANTLR4 grammars available for JavaScript/ECMAScript. We could use ANTLR’s Python runtime with a pre-existing JS grammar to parse code. This approach would generate a parse tree, and we’d write code to traverse it. However, maintaining ANTLR grammars for modern JavaScript (with new syntax features, etc.) could be challenging, and tree-sitter (or ast-grep) likely offers a more up-to-date, maintained solution.
        
    
    Given these options, **ast-grep (tree-sitter) is recommended for JavaScript**, since it's already integrated and efficient.
    
*   **TypeScript:** Ast-grep supports TypeScript via the `"typescript"` and `"tsx"` language options[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=Python%20,yaml). Using it, we can parse `.ts` files just as easily. TypeScript’s syntax for functions and classes is similar to JavaScript’s, with the addition of type annotations and access modifiers. The AST patterns can accommodate those (for example, a TypeScript class method might be declared with `public methodName(...) { ... }` – our pattern might use wildcards to skip modifiers or capture them if needed). Alternatives include:
    
    *   _TypeScript Compiler API:_ TypeScript’s own compiler (tsc) can produce an AST (or more specifically, it has a JSON AST output or can be accessed via Node.js). However, leveraging this from Python would require running an external process or using a Node binding, which complicates the Python tool pipeline.
        
    *   _ANTLR:_ There are TypeScript grammars (often based on the ECMAScript grammar plus types). Similar caveats as with JS – maintaining it is non-trivial.
        
    *   _Tree-sitter:_ Tree-sitter has a TypeScript grammar that ast-grep already uses. We could use tree-sitter directly as well, similar to JS.
        
    
    Again, **ast-grep is the straightforward choice for TypeScript**. It will handle parsing TS syntax, including modern features, and we can focus on pattern matching (for example, include patterns to catch `constructor(...) { ... }` in classes, etc., since constructors in classes are a special kind of method).
    
*   **C++:** Ast-grep includes support for C++ via the `"cpp"` language alias[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=,hs). This uses tree-sitter-cpp, which is capable of parsing C++17 (and likely beyond) syntax reasonably well. We can rely on it to parse .cpp and .hpp files and then use patterns to find:
    
    *   Function definitions: As mentioned, patterns may need to allow for return type and possibly qualifiers. If ast-grep’s pattern syntax is powerful enough, we might do something like `"$RET:type $FUNC($$$) { $$$ }"` (if it supports a `:type` annotation to restrict $RET to a type node) or simply use placeholders to absorb the return type. We might use multiple patterns to cover different styles (functions with no explicit return type keyword, like constructors or conversion operators, etc.). We should test patterns on sample C++ code to refine them.
        
    *   Class/struct definitions: We’ll match `class` and `struct` blocks. We may also include `namespace $NS { $$$ }` if we want to handle functions inside namespaces, though for outline purposes, it might be acceptable to show the fully qualified name or treat namespace-scoped functions as top-level (since from a single file perspective, they are top-level in that file). This is a design decision.
        
    *   Methods inside class definitions: Within a class AST node, we can find all method declarations that have bodies. In C++, methods can be declared inside class (which is an inline definition if they have a body, or just a declaration if they end in `;`). We only want those with bodies for our outline (to mirror actual implementation in the file). We can pattern-match inside class bodies for method definitions, e.g. `"$RET $METHOD($$$) { $$$ }"` inside the class node, which will catch inline-defined methods.
        
    *   Out-of-class method definitions (as noted earlier): One strategy is after collecting all class definitions, also collect any free function whose name contains `::`. If a function name is qualified like `SomeClass::MethodName`, we can interpret that as a class method implementation. We could then attach that to `SomeClass` in the outline. Implementing this grouping might require parsing the text of the function name or using ast-grep patterns that directly capture the qualifier (perhaps a pattern like `"$CLASS::$METHOD($$$) { $$$ }"` to find those definitions). This is a bit advanced, but it would greatly enhance the C++ outline readability.
        
    
    Other tools for C++ include:
    
    *   _Clang/Libclang:_ The Clang compiler provides a C/C++ AST through its libraries. There is a Python binding (`libclang` via `clang.cindex`) that can parse C++ source properly (including macro resolution, if configured). Using libclang, we could get a detailed AST and query for functions and classes. This is very powerful and accurate (it truly parses C++ the same way a compiler would), but it introduces a heavy dependency on LLVM/Clang and is more complex to integrate. It might be overkill for simply listing functions and classes, especially since tree-sitter (and thus ast-grep) can do the job more lightly.
        
    *   _ctags-like tools:_ Tools like Universal Ctags can list definitions in code. However, ctags is regex-based and may not capture start-end lines or distinguish inner vs outer functions as reliably as an AST approach. Since we already depend on ast-grep, we have a solid AST solution.
        
    *   _ANTLR:_ Historically, creating a full C++ grammar for ANTLR has been very difficult due to C++ complexity. There are some grammars out there, but keeping them up to date with all language features is challenging. This is generally not recommended when alternatives like Clang or tree-sitter exist.
        
    
    **Recommendation:** Continue using ast-grep for C++ parsing. The tree-sitter C++ parser should handle the majority of C++ syntax. We will focus on writing robust patterns and possibly some custom logic to handle out-of-class method groupings.
    
*   **C:** Ast-grep supports C (language alias `"c"`)[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=Language%20Name%20Alias%20File%20Extension,exs) via a tree-sitter-c grammar. This is quite straightforward compared to C++:
    
    *   We will gather all top-level function definitions. Patterns can be similar to C++ (e.g., `"${RET} $FUNC($$$) { $$$ }"`). In C, there are no namespaces or classes, so every function is effectively global. We should still ensure we exclude any prototypes (declarations ending with `;`). A pattern including the function body braces will naturally do that.
        
    *   C doesn’t have methods, so we don’t have to worry about inner functions except nested functions which are actually a GCC extension (not standard C90/C99). Those are rare and we might ignore them.
        
    *   One might consider listing `struct` or `enum` definitions as part of an outline. If desired, we could add pattern `"$KW $NAME { $$$ };"` where `$KW` is `struct` or `union` or `enum` to list type definitions. But since the original Python tool focuses on functions and classes, for consistency we might skip C `struct` listings (they are more like data definitions, not code routines).
        
    
    Alternatives for C parsing include:
    
    *   _pycparser:_ A pure-Python C parser that can handle C99 (without macros). `pycparser` generates an AST for C code. It could be used to find function definitions (it provides node types for FuncDef). This is a lightweight option if we didn't have ast-grep. However, it doesn’t handle macros or C11/17 features, whereas tree-sitter’s C grammar (and thus ast-grep) covers a broad range and can simply skip macro lines as needed.
        
    *   _Clang:_ As with C++, libclang can parse C accurately. The considerations are similar (accuracy vs dependency weight).
        
    *   _ANTLR:_ There is an official ANTLR4 C grammar (provided as an example in the ANTLR repository). It can parse C pretty well and could be used with the ANTLR Python runtime. You’d get a parse tree and would have to walk it to find functions (looking for parser rule contexts representing function definitions). This is doable, but given we already have ast-grep in use, it’s an unnecessary complexity.
        

In conclusion, **leveraging ast-grep for all the new languages is the most efficient approach**. It gives us a unified API for parsing and querying, which aligns with how the Python support is implemented. It’s effectively using tree-sitter under the hood for each language, which is a proven approach for parsing source code in tools[stackoverflow.com](https://stackoverflow.com/questions/65076264/python-library-for-parsing-code-of-any-language-into-an-ast#:~:text=The%20library%20tree,binding%2C%20tons%20of%20language%20parsers). Should ast-grep ever lack support or have limitations for a specific language, the alternatives mentioned (esprima for JS, pycparser for C, libclang for C++, etc.) can be considered. But as of now, ast-grep supports 20+ languages including our targets, making it a one-stop solution.

Potential Pitfalls and Limitations in Generalizing the Pipeline
---------------------------------------------------------------

Generalizing the outline generator to multiple languages introduces several challenges and potential pitfalls:

*   **Syntax Differences:** Each language has unique syntax quirks that might not fit neatly into the pattern matching approach used for Python. For instance:
    
    *   In Python, function definitions are always clearly marked by `def` at the start of a line. In C/C++, function definitions start with a return type (which could be a complex declarator), and there’s no single token that signals “here begins a function” – making pattern matching trickier. We must ensure our patterns are broad enough to catch various return types (including pointers, const qualifiers, templates, etc.) without accidentally matching things that aren’t function definitions.
        
    *   JavaScript has multiple ways to define functions (declarations, expressions, arrow functions). We need to decide which forms to include. Omitting some (like anonymous functions or immediately-invoked function expressions) is usually fine for an outline, but we should handle at least named function declarations and class methods. Arrow functions without names (lambdas) likely don’t belong in a high-level outline unless assigned to a variable.
        
    *   TypeScript’s type annotations could complicate pattern matching if not accounted for. For example, a TS function can be `function foo(arg: Type): ReturnType { ... }`. If our pattern is too simple, we might miss functions with type annotations or overload signatures. We should test patterns against typical TS code or use ast-grep’s ability to match AST nodes rather than exact text to handle this.
        
    *   C++ has overloads, templates, and special member functions (constructors, destructors, operators). Our outline might not need special handling beyond listing them, but our pattern should catch constructors (which have no return type and same name as class) and perhaps skip listing the implicit ones. A constructor inside a class will be found as a method (with name `CLASS` in the AST perhaps). A constructor defined outside (unlikely in C++, usually they are inside class definition if provided inline) would appear as `ClassName::ClassName(...)`. Our patterns should be aware that `$RET` might be empty in such cases (or we specifically pattern for that).
        
    *   Preprocessor directives in C/C++ can disrupt parsing or cause ast-grep to see code differently. Tree-sitter C/C++ tries to handle macros by treating them as nodes or skipping them, but complex macro usage might cause either parse errors or incomplete AST. This might rarely affect the outline (since macros could generate code or guard definitions). It’s a minor concern, but worth noting if parse failures occur – in such cases, a fallback or at least a clear error message would be needed.
        
*   **AST Query Complexity:** Using structural patterns for each language means we rely on ast-grep’s pattern engine. While ast-grep is powerful, crafting the right patterns may require knowledge of how the AST nodes are constructed. If our patterns are too naive, we might:
    
    *   Miss some definitions (false negatives) – e.g., if we forget to include a pattern for a function with no parameters vs some parameters, etc. (The `$$$` wildcard helps cover “any code” in ast-grep patterns, which is very useful.)
        
    *   Capture things we don't want (false positives) – e.g., a pattern that’s too general might match something that isn't actually a top-level function. However, since ast-grep uses actual AST, this risk is lower than text-based grep. We should still be careful; for instance, a C pattern like `"$FUNC($$$) { $$$ }"` might match a lambda expression in C++ if not anchored properly, or a function inside a class if used globally. We rely on context (like doing `node.find_all` on the root for top-level, and `cls.find_all` inside classes) to mitigate this.
        
    *   Overlapping matches: The approach of “find all functions then subtract those inside classes” works but could get more complex if we have nested structures. For example, JavaScript can have free-standing functions inside an immediately invoked function (IIFE) which is inside a file. Those are technically not global, but our simplistic filter (only removing those inside classes) would still list them. A more general approach is needed if we want strictly top-level only. We should consider implementing a check for the parent node type: only treat function nodes whose parent is the top-level program (or module) node as global. This capability depends on ast-grep’s API (it might allow checking the kind of parent node or we can infer by absence of a class/func parent).
        
*   **Grouping and Ordering:** In multi-language projects, especially C/C++, the order in which items appear in a file might not strictly reflect a logical grouping. For instance, a C++ file might have a class definition at the top and related free functions later. Our current approach simply lists functions in the order found. If we manage to group out-of-class `ClassName::method` definitions under the class, we will be presenting them out of textual order (which is okay for logical grouping, but we should indicate they were found in that file and their line numbers). Also, if the file contains multiple classes and multiple free functions, we should ensure the outline ordering remains clear (possibly segregating by class vs free functions).
    
*   **Performance Considerations:** As we add support for more languages, particularly with large codebases:
    
    *   Parsing many files with ast-grep (tree-sitter) is generally fast, but the complexity of C++ parsing might impact performance. Tree-sitter C++ is quite performant in Rust, and ast-grep likely handles multithreading internally for search[ast-grep.github.io](https://ast-grep.github.io/#:~:text=Performant). Still, we should test the tool on a directory with many files to ensure it’s responsive.
        
    *   The initial Python implementation reads files fully into memory and constructs ASTs one by one. For very large files (especially in C++), memory usage could be high. We might consider processing files one at a time and streaming results out, rather than building one giant string of output, but given typical usage (outline generation is often on moderate code bases or single files), this is probably fine.
        
*   **Dependency Management:** Introducing different parsing libraries for different languages could bloat the project. Luckily, ast-grep’s single dependency covers all. If, however, we faced a case where ast-grep doesn’t support a needed language (not in our current list, but hypothetically for future languages), we might bring in another library (like ANTLR or a specialized parser). Mixing parsing libraries means different data structures for ASTs, which complicates the outline generation pipeline. It’s best to stick with one unified approach per design. Thus a pitfall to avoid is having divergent code paths for each language using entirely different tools, as that would increase maintenance burden significantly. Using ast-grep everywhere avoids this pitfall, leveraging a common API for AST queries.
    
*   **Testing and Accuracy:** With multiple languages, ensuring the outline is correct in all cases requires thorough testing. Each language will need example files to verify that:
    
    *   All intended constructs are captured (e.g., do we list that free-standing arrow function? Is an overloaded C++ function listed once? Are inner JavaScript functions excluded properly? etc.).
        
    *   The line ranges are correct (tree-sitter provides start and end lines; ast-grep’s `range()` should handle this, but off-by-one errors need to be checked as we saw the code adding 1 to convert 0-indexed lines to 1-indexed[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py)).
        
    *   No syntax errors in code cause crashes. For example, if the user points the tool to a file with syntax errors, ast-grep might throw an exception or simply not find matches. The current Python code catches file read errors but not parse errors. We might need to handle parse failures (perhaps ast-grep returns an empty root or throws) and report them gracefully (e.g., “❌ Could not parse file X”).
        
*   **Cross-language Interaction:** If the tool ever needed to outline a project that contains multiple languages together (say a directory with some .py, .js, .cpp files mixed), we’d have to decide how to handle it. The straightforward approach is to require one language at a time (the user specifies or invokes the appropriate tool). Auto-detecting language per file in a single run is possible (ast-grep can infer from extension), but merging the output of different languages might not be very meaningful unless grouped by file. It’s probably out of scope to outline multiple languages in one invocation, but worth clarifying in documentation.
    

In essence, the main limitations will revolve around correctly adapting the outline extraction logic to each language’s structure and ensuring we don’t misidentify or omit important definitions. By carefully crafting patterns and augmenting our filtering logic (e.g., parent context checks), we can avoid most pitfalls. The **complexity of C++** is the highest risk area – we should be prepared for tweaking patterns or using minor post-processing (like splitting qualified names) to get a nice outline. Nonetheless, tree-sitter (via ast-grep) provides a solid foundation, and many projects have successfully handled multi-language parsing using it, indicating it’s a reliable path[ast-grep.github.io](https://ast-grep.github.io/#:~:text=Polyglot)[stackoverflow.com](https://stackoverflow.com/questions/65076264/python-library-for-parsing-code-of-any-language-into-an-ast#:~:text=The%20library%20tree,binding%2C%20tons%20of%20language%20parsers).

Design for Scalable Addition of Languages
-----------------------------------------

To ensure that adding new languages in the future is as smooth as possible, a clear **modular design** should be adopted now. Here are the steps and design patterns that will make the outline generator extensible:

1.  **Introduce a Language Abstraction:** Create a structure to hold language-specific parsing rules. This can be an abstract class or interface, or simply a data structure. For example, define a base class `OutlineGenerator` with a method like `get_outline(content:str) -> List[OutlineItem]`. Then implement subclasses for each language (Python, JavaScript, etc.) that override:
    
    *   How to initialize the parser (i.e., what language string to pass to `SgRoot`).
        
    *   What patterns to search for top-level functions, classes, and class methods.
        
    *   Any special filtering needed for that language (e.g., grouping C++ out-of-class methods, or skipping certain constructs).
        
    
    Using a class hierarchy is a classic **Strategy Pattern**: the overall algorithm for generating outlines can remain in a higher-level coordinator, which delegates the language-specific parts to the appropriate strategy object. For example, a `LanguageStrategy` interface with methods `find_functions(root)` and `find_classes(root)` could be defined. The Python strategy’s `find_functions` uses the Python patterns, the C++ strategy’s uses C++ patterns, and so on. The main routine then simply does: `nodes_funcs = strategy.find_functions(ast_root); nodes_classes = strategy.find_classes(ast_root)` and processes the results generically.
    
2.  **Language Registry:** Maintain a mapping from file extension or language name to the corresponding strategy or configuration. This could be as simple as a dict: `LANGUAGES = {"python": PythonOutlineGenerator(), "javascript": JSOutlineGenerator(), ...}`. If the user passes a `language` identifier, we use the corresponding strategy. If the user provides just a file path, we can infer the language by the file extension and look it up in this map. Ast-grep itself can auto-detect by extension, which we might leverage, but being explicit is safer to avoid ambiguity (e.g., “.h” could be C or C++). A registry also makes it easy to add a new language: just implement a new strategy class and add an entry to the map.
    
3.  **Unified Outline Data Structure:** Have a common data structure for outline items (e.g., a simple class or tuple that holds `name`, `type` (function or class), `start_line`, `end_line`, and maybe `parent_name` for methods). Each language strategy can produce a list of these outline items from the AST. The main code then handles sorting/grouping and formatting. By decoupling data gathering from formatting, we make the addition of new languages just a matter of producing the right list of items. The formatting (adding icons, indenting methods under classes, etc.) can be done in a generic way by the main module using the `type` and `parent` information in the outline items.
    
4.  **Reuse Common Logic:** Identify code that can be shared:
    
    *   File reading and error handling is the same for all languages.
        
    *   Distinguishing between file vs directory input is common; only the file extension filter changes.
        
    *   The final assembly of output strings can be mostly common, perhaps with slight variations in keyword or icon if desired. We could parameterize the icons or labels in the language config (for example, some might want a different icon for a JavaScript function, but likely the icons remain consistent).
        
    *   The MCP server integration can remain mostly unchanged; we’ll either have multiple tool functions or one that calls the appropriate strategy. In either case, we can avoid duplicating the entire file scanning and printing logic for each tool by calling a shared function internally.
        
5.  **Scalable File Discovery:** For scalability, consider supporting multi-language projects by allowing the user to specify multiple languages or auto-detect. While not a priority for now, designing the file discovery in a modular way can help. For example, the `process_folder` function could accept a list of file extensions or a language and then consult the extension map. In the future, one could extend it to `process_folder(path, languages=["python","javascript"])` to handle multiple at once. Internally it would gather files for each language type and perhaps produce separate sections. This isn’t strictly required by the prompt, but thinking in this direction ensures the design isn’t needlessly limited.
    
6.  **Testing and Examples:** Develop small example files for each supported language and write unit tests for the outline output. This not only guards against regressions as more languages are added but also serves as documentation for how the outline looks for each language. For instance, having a sample JavaScript file with a couple of functions and classes, and verifying that `js_outline("sample.js")` returns the expected formatted string. This practice will make it easier to add a new language—one can create a sample file, implement the strategy, and quickly see if the output matches expectations.
    
7.  **Documentation and Extensibility:** Clearly document how a new language can be added. For example: “To add a new language, provide a tree-sitter grammar or ensure ast-grep supports it, then write a new strategy specifying patterns for function and class extraction.” If ast-grep supports dynamic loading of custom grammars[ast-grep.github.io](https://ast-grep.github.io/#:~:text=Supports%20many%20programming%20languages%20out,sitter%20parsers%20by%20dynamic%20loading), we could even allow advanced users to plug in a grammar for a language not built-in (like say someone wants outlines for Pascal, etc.). Our architecture should handle an unknown language by either raising a clear error or by using a plugin if provided.
    

By following these steps, we embrace a design where adding a language is **modular and isolated** – one doesn’t have to touch the core logic, just add a new module that knows that language’s syntax. The use of the Strategy pattern or a similar modular approach ensures that as the list of supported languages grows, the codebase remains organized. Each language module can be maintained separately, and improvements or bug fixes in one (e.g., refining a C++ pattern) won’t risk breaking others.

In terms of **design patterns**, aside from Strategy, we also effectively use a **Factory pattern** when we choose the parser/strategy based on language input. The `LANGUAGES` registry acts as a factory for the appropriate outline generator. Additionally, using an intermediate representation (the outline items list) is an application of the **Adapter pattern**, converting AST nodes (which differ by language) into a uniform list of entries that the rest of the program can handle uniformly.

Finally, by keeping the parsing library consistent (ast-grep for all), we ensure the scalability in terms of maintenance: updates to ast-grep (e.g., improvements in tree-sitter grammars or bug fixes) will benefit all languages uniformly. This unified approach is easier to scale than juggling multiple parsing technologies.

* * *

**In summary**, to add JavaScript, TypeScript, C++, C (and future languages) support, we should refactor the one-off Python script into a more generalized framework. This involves abstracting language-specific details, leveraging ast-grep’s multi-language capabilities, and being mindful of each language’s quirks. With a clean modular design, the outline generator can evolve from a Python-only tool into a scalable multi-language code outline solution, while minimizing duplication and ensuring maintainability. The changes will enable us to generate structured outlines for each target language, using appropriate parsing libraries (with tree-sitter/ast-grep being central), and set up an architecture that can grow as new languages or requirements emerge. Each of the focus areas – from parsing to pattern design to pipeline adjustments – plays a role in this transformation, and with careful implementation, the result will be a robust, extensible outline generator supporting the prioritized languages and beyond.

**Sources:**

*   Code from _OhadRubin/python-outline-mcp_ showing current Python-specific implementation[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py)[GitHub](https://github.com/OhadRubin/python-outline-mcp/blob/b8e566e29add8d7b076771db4f3a3c307af4e264/outline.py).
    
*   ast-grep documentation indicating multi-language (tree-sitter) support[ast-grep.github.io](https://ast-grep.github.io/#:~:text=Polyglot)[ast-grep.github.io](https://ast-grep.github.io/reference/languages.html#:~:text=,hs).
    
*   Stack Overflow discussion recommending tree-sitter for parsing multiple languages in Python[stackoverflow.com](https://stackoverflow.com/questions/65076264/python-library-for-parsing-code-of-any-language-into-an-ast#:~:text=The%20library%20tree,binding%2C%20tons%20of%20language%20parsers).

## Prompt:
please write that functionality for javascript.

## Response:
Request for o3 pro

Reasoned for 17m 27s

Below is a self‑contained module **`outline_js.py`** that mirrors the current Python outline tool but targets **JavaScript** files (`.js`, `.jsx`).  
It depends on **ast‑grep**—the same dependency already used—so no new libraries are required.

```python
"""
outline_js.py
Generate a hierarchical outline (top‑level functions, classes, class methods)
for JavaScript source files or folders.

Usage (script):
    python outline_js.py path/to/file_or_folder [--no-recursive]

Usage (from code):
    from outline_js import js_outline
    print(js_outline("example.js"))
"""

from pathlib import Path
import subprocess
import sys

try:
    from sg import SgRoot       # ast‑grep Python binding
except ImportError as e:
    raise RuntimeError(
        "ast‑grep (pip install ast-grep-python) must be available."
    ) from e


# ---------- patterns ----------
FUNC_PATTERNS = [
    "function $FUNC($$$) { $$$ }",
    "export function $FUNC($$$) { $$$ }",
    "async function $FUNC($$$) { $$$ }",
    "export async function $FUNC($$$) { $$$ }",
]

CLASS_PATTERNS = [
    "class $CLASS { $$$ }",
    "class $CLASS extends $$$ { $$$ }",
    "export class $CLASS { $$$ }",
    "export class $CLASS extends $$$ { $$$ }",
]

METHOD_PATTERNS = [
    "$METHOD($$$) { $$$ }",
    "static $METHOD($$$) { $$$ }",
    "async $METHOD($$$) { $$$ }",
    "static async $METHOD($$$) { $$$ }",
]


# ---------- helpers ----------
def _dedup(nodes):
    seen = set()
    uniq = []
    for n in nodes:
        key = (n.range().start.byte, n.range().end.byte)
        if key not in seen:
            seen.add(key)
            uniq.append(n)
    return uniq


def _inside(inner, outer):
    return (
        inner.range().start.byte >= outer.range().start.byte
        and inner.range().end.byte <= outer.range().end.byte
    )


def _outline_file(path: Path) -> str:
    content = path.read_text(encoding="utf‑8")
    root = SgRoot(content, "javascript")

    # collect raw matches
    func_nodes = []
    for pat in FUNC_PATTERNS:
        func_nodes.extend(root.find_all(pat))
    func_nodes = _dedup(func_nodes)

    class_nodes = []
    for pat in CLASS_PATTERNS:
        class_nodes.extend(root.find_all(pat))
    class_nodes = _dedup(class_nodes)

    # filter top‑level functions (not inside any class)
    toplevel_funcs = [
        n
        for n in func_nodes
        if not any(_inside(n, c) for c in class_nodes)
    ]

    # build outline lines
    lines = []
    header = f"📁 {path}"
    lines.append(header)
    lines.append("-" * len(header))

    for fn in toplevel_funcs:
        name = fn["FUNC"].text()
        rng = fn.range()
        lines.append(
            f"⚙️  def {name} [{rng.start.line+1}:{rng.end.line+1}]"
        )

    for cls in class_nodes:
        cls_name = cls["CLASS"].text()
        rng_cls = cls.range()
        lines.append(
            f"🏛️  class {cls_name} [{rng_cls.start.line+1}:{rng_cls.end.line+1}]"
        )

        # methods within this class
        methods = []
        for pat in METHOD_PATTERNS:
            methods.extend(cls.find_all(pat))
        methods = _dedup(methods)

        for m in methods:
            meth_name = m["METHOD"].text()
            rng_m = m.range()
            lines.append(
                f"    🔧 def {meth_name} [{rng_m.start.line+1}:{rng_m.end.line+1}]"
            )

    return "\n".join(lines) + "\n"


def _iter_js_files(folder: Path, recursive: bool):
    exts = [".js", ".jsx"]
    if (folder / ".git").is_dir():
        # respect gitignore
        args = ["git", "-C", str(folder), "ls-files"]
        tracked = subprocess.check_output(args, text=True).splitlines()
        for f in tracked:
            p = folder / f
            if p.suffix in exts:
                yield p
    else:
        pattern = "**/*" if recursive else "*"
        for p in folder.glob(pattern):
            if p.is_file() and p.suffix in exts:
                yield p


# ---------- public API ----------
def js_outline(path: str | Path, recursive: bool = True) -> str:
    """
    Return an outline string for a JavaScript file or folder.

    Parameters
    ----------
    path : str | Path
        File path or directory.
    recursive : bool
        When path is a directory, recurse into subfolders.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    if path.is_file():
        return _outline_file(path)

    outlines = []
    for f in _iter_js_files(path, recursive):
        outlines.append(_outline_file(f))
    return "\n".join(outlines)


# ---------- CLI ----------
if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Generate JS outline")
    ap.add_argument("path", help="JavaScript file or directory")
    ap.add_argument("--no-recursive", action="store_true", help="non‑recursive folder scan")
    opts = ap.parse_args()

    print(js_outline(opts.path, recursive=not opts.no_recursive))
```

### Integration Steps

1.  **Place** `outline_js.py` in the repository root (next to the existing Python outline script).
    
2.  **Add** `ast-grep-python` to `requirements.txt` if not already present:
    
    ```
    ast-grep-python>=0.19
    ```
    
3.  **(Optional)** Extend the MCP server:
    
    ```python
    # in server startup code
    from outline_js import js_outline
    server.add_tool(
        name="js_outline",
        func=js_outline,
        description="Return outline for .js/.jsx files"
    )
    ```
    
4.  **Test**:
    
    ```bash
    python outline_js.py examples/sample.js
    ```
    

This module follows the same conventions (icons, line numbers) as the original Python tool, giving consistent output for JavaScript code.

## Prompt:
please write that functionality for typescript

## Response:
Request for o3 pro

Reasoned for 2m 14s

Below is **`outline_ts.py`**.  
It mirrors the JavaScript module but targets **TypeScript** files (`.ts`, `.tsx`).  
Dependency remains **ast‑grep**.

```python
"""
outline_ts.py
Generate an outline (top‑level functions, classes, class methods)
for TypeScript source files or folders.

CLI:
    python outline_ts.py path/to/item [--no-recursive]

Code use:
    from outline_ts import ts_outline
    outline_str = ts_outline("example.ts")
"""

from pathlib import Path
import subprocess
import sys

try:
    from sg import SgRoot          # ast‑grep binding
except ImportError as e:
    raise RuntimeError(
        "Install ast-grep-python:  pip install ast-grep-python"
    ) from e


# ---------- pattern tables ----------
FUNC_PATTERNS = [
    # without return type
    "function $FUNC($$$) { $$$ }",
    "export function $FUNC($$$) { $$$ }",
    "async function $FUNC($$$) { $$$ }",
    "export async function $FUNC($$$) { $$$ }",
    # with return type
    "function $FUNC($$$): $$$ { $$$ }",
    "export function $FUNC($$$): $$$ { $$$ }",
    "async function $FUNC($$$): $$$ { $$$ }",
    "export async function $FUNC($$$): $$$ { $$$ }",
]

CLASS_PATTERNS = [
    "class $CLASS { $$$ }",
    "class $CLASS extends $$$ { $$$ }",
    "export class $CLASS { $$$ }",
    "export class $CLASS extends $$$ { $$$ }",
]

# common method variants
_METHOD_BASES = [
    "$METHOD($$$)",
    "async $METHOD($$$)",
    "static $METHOD($$$)",
    "static async $METHOD($$$)",
    "public $METHOD($$$)",
    "private $METHOD($$$)",
    "protected $METHOD($$$)",
    "public async $METHOD($$$)",
    "private async $METHOD($$$)",
    "protected async $METHOD($$$)",
    "public static $METHOD($$$)",
    "private static $METHOD($$$)",
    "protected static $METHOD($$$)",
    "public static async $METHOD($$$)",
    "private static async $METHOD($$$)",
    "protected static async $METHOD($$$)",
]

METHOD_PATTERNS = []
for base in _METHOD_BASES:
    METHOD_PATTERNS.append(f"{base} {{ $$$ }}")            # no return type
    METHOD_PATTERNS.append(f"{base}: $$$ {{ $$$ }}")       # with return type


# ---------- helpers ----------
def _dedup(nodes):
    seen = set()
    out = []
    for n in nodes:
        key = (n.range().start.byte, n.range().end.byte)
        if key not in seen:
            seen.add(key)
            out.append(n)
    return out


def _inside(inner, outer):
    return (
        inner.range().start.byte >= outer.range().start.byte
        and inner.range().end.byte <= outer.range().end.byte
    )


def _outline_file(path: Path) -> str:
    content = path.read_text(encoding="utf-8", errors="ignore")
    # choose language alias for ast‑grep
    lang = "tsx" if path.suffix == ".tsx" else "typescript"
    root = SgRoot(content, lang)

    funcs, classes = [], []

    for pat in FUNC_PATTERNS:
        funcs.extend(root.find_all(pat))
    funcs = _dedup(funcs)

    for pat in CLASS_PATTERNS:
        classes.extend(root.find_all(pat))
    classes = _dedup(classes)

    top_funcs = [n for n in funcs if not any(_inside(n, c) for c in classes)]

    lines = []
    head = f"📁 {path}"
    lines.append(head)
    lines.append("-" * len(head))

    for fn in top_funcs:
        name = fn["FUNC"].text()
        rng = fn.range()
        lines.append(f"⚙️  def {name} [{rng.start.line+1}:{rng.end.line+1}]")

    for cls in classes:
        cls_name = cls["CLASS"].text()
        rng_c = cls.range()
        lines.append(f"🏛️  class {cls_name} [{rng_c.start.line+1}:{rng_c.end.line+1}]")

        methods = []
        for pat in METHOD_PATTERNS:
            methods.extend(cls.find_all(pat))
        methods = _dedup(methods)

        for m in methods:
            mname = m["METHOD"].text()
            rng_m = m.range()
            lines.append(f"    🔧 def {mname} [{rng_m.start.line+1}:{rng_m.end.line+1}]")

    return "\n".join(lines) + "\n"


def _iter_ts_files(folder: Path, recursive: bool):
    exts = [".ts", ".tsx"]
    if (folder / ".git").is_dir():
        files = subprocess.check_output(
            ["git", "-C", str(folder), "ls-files"], text=True
        ).splitlines()
        for f in files:
            p = folder / f
            if p.suffix in exts:
                yield p
    else:
        pattern = "**/*" if recursive else "*"
        for p in folder.glob(pattern):
            if p.is_file() and p.suffix in exts:
                yield p


# ---------- public API ----------
def ts_outline(path: str | Path, recursive: bool = True) -> str:
    """
    Return outline for a TypeScript file or directory.

    Parameters
    ----------
    path : str | Path
        File or folder.
    recursive : bool
        Recurse when path is a folder.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    if path.is_file():
        return _outline_file(path)

    outlines = []
    for f in _iter_ts_files(path, recursive):
        outlines.append(_outline_file(f))
    return "\n".join(outlines)


# ---------- CLI ----------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate TypeScript outline")
    parser.add_argument("path", help=".ts or .tsx file, or folder")
    parser.add_argument("--no-recursive", action="store_true")
    opts = parser.parse_args()

    print(ts_outline(opts.path, recursive=not opts.no_recursive))
```

### Integration

1.  Save the file in the repository root.
    
2.  Ensure `ast-grep-python` is listed in **requirements.txt**.
    
3.  Optionally expose an MCP tool:
    

```python
from outline_ts import ts_outline
server.add_tool(
    name="ts_outline",
    func=ts_outline,
    description="Return outline for .ts/.tsx files"
)
```

4.  Run a quick check:
    

```bash
python outline_ts.py src/example.ts
```

## Prompt:
now for c++

## Response:
Request for o3 pro

Reasoned for 3m 3s

Below is **`outline_cpp.py`**.  
It follows the same structure as the earlier JS and TS modules and uses **ast‑grep** to parse **C++** files.

```python
"""
outline_cpp.py
Generate an outline of top‑level functions, classes/structs, and methods
for C++ source files or folders.

Command‑line:
    python outline_cpp.py path/to/item [--no-recursive]

Code use:
    from outline_cpp import cpp_outline
    txt = cpp_outline("example.cpp")
"""

from pathlib import Path
import subprocess

try:
    from sg import SgRoot           # ast‑grep binding
except ImportError as e:
    raise RuntimeError(
        "Install ast-grep-python:  pip install ast-grep-python"
    ) from e


# ---------- patterns ----------
FUNC_PATTERNS = [
    "$RET $FUNC($$$) { $$$ }",
    "$FUNC($$$) { $$$ }",                        # constructors / destructors
    "template <$$$> $RET $FUNC($$$) { $$$ }",
    "template <$$$> $FUNC($$$) { $$$ }",
]

CLASS_PATTERNS = [
    "class $CLASS { $$$ };",
    "class $CLASS { $$$ }",
    "struct $CLASS { $$$ };",
    "struct $CLASS { $$$ }",
]

METHOD_PATTERNS = [
    "$RET $METHOD($$$) { $$$ }",
    "$METHOD($$$) { $$$ }",
    "~$METHOD($$$) { $$$ }",                    # destructor
]

OUTSIDE_METHOD_PATTERNS = [
    "$QUAL::$METHOD($$$) { $$$ }",
    "template <$$$> $QUAL::$METHOD($$$) { $$$ }",
]


# ---------- helpers ----------
def _dedup(nodes):
    seen = set()
    out = []
    for n in nodes:
        key = (n.range().start.byte, n.range().end.byte)
        if key not in seen:
            seen.add(key)
            out.append(n)
    return out


def _inside(inner, outer):
    return (
        inner.range().start.byte >= outer.range().start.byte
        and inner.range().end.byte <= outer.range().end.byte
    )


def _outline_file(path: Path) -> str:
    code = path.read_text(encoding="utf-8", errors="ignore")
    root = SgRoot(code, "cpp")

    # collect classes
    cls_nodes = []
    for p in CLASS_PATTERNS:
        cls_nodes.extend(root.find_all(p))
    cls_nodes = _dedup(cls_nodes)

    # collect top‑level functions
    fn_nodes = []
    for p in FUNC_PATTERNS:
        fn_nodes.extend(root.find_all(p))
    fn_nodes = _dedup(fn_nodes)

    # exclude functions inside any class block
    top_funcs = [n for n in fn_nodes if not any(_inside(n, c) for c in cls_nodes)]

    # group inline methods inside classes
    cls_methods = {c["CLASS"].text(): [] for c in cls_nodes}
    for c in cls_nodes:
        for pat in METHOD_PATTERNS:
            ms = c.find_all(pat)
            for m in ms:
                cls_methods[c["CLASS"].text()].append(m)

    # collect out‑of‑class method definitions and attach
    outside_meth_nodes = []
    for p in OUTSIDE_METHOD_PATTERNS:
        outside_meth_nodes.extend(root.find_all(p))
    outside_meth_nodes = _dedup(outside_meth_nodes)

    for n in outside_meth_nodes:
        qual = n["QUAL"].text()
        parts = qual.split("::")
        cls_name = parts[-1] if parts else qual
        cls_methods.setdefault(cls_name, []).append(n)

    # build outline
    lines = []
    head = f"📁 {path}"
    lines.append(head)
    lines.append("-" * len(head))

    for fn in top_funcs:
        name = fn["FUNC"].text()
        rng = fn.range()
        lines.append(f"⚙️  def {name} [{rng.start.line+1}:{rng.end.line+1}]")

    for cls in cls_nodes:
        cname = cls["CLASS"].text()
        rng_c = cls.range()
        lines.append(f"🏛️  class {cname} [{rng_c.start.line+1}:{rng_c.end.line+1}]")

        for m in cls_methods.get(cname, []):
            mname = m["METHOD"].text()
            rng_m = m.range()
            lines.append(f"    🔧 def {mname} [{rng_m.start.line+1}:{rng_m.end.line+1}]")

    # include out‑of‑class methods whose class was not declared in this file
    declared_cls = {c["CLASS"].text() for c in cls_nodes}
    for cls_name, mlist in cls_methods.items():
        if cls_name in declared_cls:
            continue
        lines.append(f"🏛️  class {cls_name} [external]")
        for m in mlist:
            mname = m["METHOD"].text()
            rng_m = m.range()
            lines.append(f"    🔧 def {mname} [{rng_m.start.line+1}:{rng_m.end.line+1}]")

    return "\n".join(lines) + "\n"


def _iter_cpp_files(folder: Path, recursive: bool):
    exts = [".cpp", ".cc", ".cxx", ".hpp", ".hh", ".h"]
    if (folder / ".git").is_dir():
        files = subprocess.check_output(
            ["git", "-C", str(folder), "ls-files"], text=True
        ).splitlines()
        for f in files:
            p = folder / f
            if p.suffix in exts:
                yield p
    else:
        patt = "**/*" if recursive else "*"
        for p in folder.glob(patt):
            if p.is_file() and p.suffix in exts:
                yield p


# ---------- public API ----------
def cpp_outline(path: str | Path, recursive: bool = True) -> str:
    """
    Return an outline for C++ code.

    Parameters
    ----------
    path : str | Path
        File or directory.
    recursive : bool
        Recurse when path is a folder.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    if path.is_file():
        return _outline_file(path)

    outs = []
    for f in _iter_cpp_files(path, recursive):
        outs.append(_outline_file(f))
    return "\n".join(outs)


# ---------- CLI ----------
if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Generate C++ outline")
    ap.add_argument("path", help=".cpp/.hpp file or folder")
    ap.add_argument("--no-recursive", action="store_true")
    opt = ap.parse_args()

    print(cpp_outline(opt.path, recursive=not opt.no_recursive))
```

### Integration

1.  Save the file.
    
2.  Ensure `ast-grep-python` is listed in **requirements.txt**.
    
3.  Optionally register an MCP tool:
    

```python
from outline_cpp import cpp_outline
server.add_tool(
    name="cpp_outline",
    func=cpp_outline,
    description="Return outline for C++ files"
)
```

4.  Test:
    

```bash
python outline_cpp.py src/main.cpp
```

## Prompt:
Now do java

## Response:
Request for o3 pro

Reasoned for 19m 1s

Below is **`outline_java.py`**.  
It follows the same template used for the JS / TS / C++ modules and relies on **ast‑grep** for parsing.  
The outline lists top‑level classes / interfaces / enums / records and, for each, the methods (including constructors) defined in that file.

```python
"""
outline_java.py
Create a hierarchical outline for Java source code.

Features
--------
* Detects top‑level class, interface, enum, and record declarations.
* Lists methods and constructors inside each type.
* Works on a single .java file or a directory (recursively by default).
* Respects .gitignore when the target path is a git repository.

CLI
---
    python outline_java.py path/to/FileOrFolder [--no-recursive]

Library
-------
    from outline_java import java_outline
    print(java_outline("src", recursive=True))
"""

from pathlib import Path
import subprocess

try:
    from sg import SgRoot          # ast‑grep Python binding
except ImportError as exc:         # pragma: no cover
    raise RuntimeError(
        "ast-grep Python API missing.  Install with:\n"
        "    pip install ast-grep-python"
    ) from exc


# ───────────────────────────── Patterns ──────────────────────────────
CLASS_PATTERNS = [
    "class $CLASS { $$$ }",
    "class $CLASS extends $$$ { $$$ }",
    "class $CLASS implements $$$ { $$$ }",
    "interface $CLASS { $$$ }",
    "interface $CLASS extends $$$ { $$$ }",
    "enum $CLASS { $$$ }",
    "record $CLASS($$$) { $$$ }",          # Java 16+
]

# common modifiers to mix in front of return type
_MODIFIERS = [
    "",
    "public",
    "private",
    "protected",
    "static",
    "final",
    "abstract",
    "public static",
    "public final",
    "public abstract",
    "protected static",
    "private static",
]

METHOD_PATTERNS: list[str] = []

# normal methods (have return type)
for mods in _MODIFIERS:
    prefix = f"{mods} " if mods else ""
    METHOD_PATTERNS.append(f"{prefix}$RET $METHOD($$$) {{ $$$ }}")

# constructors (no return type)
METHOD_PATTERNS.append("$METHOD($$$) { $$$ }")                 # default/no mods
for mods in ("public", "private", "protected"):
    METHOD_PATTERNS.append(f"{mods} $METHOD($$$) {{ $$$ }}")


# ───────────────────────────── Helpers ───────────────────────────────
def _dedup(nodes):
    """Remove duplicate AST nodes (by byte range)."""
    seen = set()
    out = []
    for n in nodes:
        key = (n.range().start.byte, n.range().end.byte)
        if key not in seen:
            seen.add(key)
            out.append(n)
    return out


def _outline_file(p: Path) -> str:
    """Return outline string for one .java file."""
    root = SgRoot(p.read_text(encoding="utf-8", errors="ignore"), "java")

    # collect types
    types = []
    for pat in CLASS_PATTERNS:
        types.extend(root.find_all(pat))
    types = _dedup(types)

    # map: type‑name → list(method‑nodes)
    type_methods: dict[str, list] = {t["CLASS"].text(): [] for t in types}

    # gather methods inside the type body
    for tnode in types:
        for pat in METHOD_PATTERNS:
            type_methods[tnode["CLASS"].text()].extend(tnode.find_all(pat))
        type_methods[tnode["CLASS"].text()] = _dedup(type_methods[tnode["CLASS"].text()])

    # build outline
    header = f"📁 {p}"
    out_lines = [header, "-" * len(header)]

    for tnode in types:
        tname = tnode["CLASS"].text()
        rng_t = tnode.range()
        out_lines.append(f"🏛️  class {tname} [{rng_t.start.line+1}:{rng_t.end.line+1}]")

        for m in type_methods[tname]:
            mname = m["METHOD"].text()
            rng_m = m.range()
            out_lines.append(f"    🔧 def {mname} [{rng_m.start.line+1}:{rng_m.end.line+1}]")

    return "\n".join(out_lines) + "\n"


def _java_files(folder: Path, recursive: bool):
    """Yield .java files inside *folder*, obeying .gitignore if present."""
    if (folder / ".git").is_dir():
        listed = subprocess.check_output(
            ["git", "-C", str(folder), "ls-files", "*.java"], text=True
        ).splitlines()
        for f in listed:
            yield folder / f
    else:
        pattern = "**/*.java" if recursive else "*.java"
        yield from folder.glob(pattern)


# ───────────────────────────── Public API ────────────────────────────
def java_outline(path: str | Path, recursive: bool = True) -> str:
    """
    Generate an outline for Java code.

    Parameters
    ----------
    path : str | Path
        .java file or directory.
    recursive : bool, default True
        Recurse into sub‑folders when *path* is a directory.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    if path.is_file():
        return _outline_file(path)

    outlines = []
    for f in _java_files(path, recursive):
        outlines.append(_outline_file(f))
    return "\n".join(outlines)


# ────────────────────────────── CLI ──────────────────────────────────
if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Generate Java outline")
    ap.add_argument("path", help=".java file or directory")
    ap.add_argument("--no-recursive", action="store_true",
                    help="do not traverse sub‑directories")
    opts = ap.parse_args()

    print(java_outline(opts.path, recursive=not opts.no_recursive))
```

### Integration Notes

1.  **Save** `outline_java.py` in the repository root.
    
2.  **Dependency**: ensure `ast-grep-python` is in `requirements.txt`.
    
3.  **(Optional)** expose an MCP tool:
    

```python
from outline_java import java_outline
server.add_tool(
    name="java_outline",
    func=java_outline,
    description="Return outline for .java files"
)
```

4.  **Quick test**
    

```bash
python outline_java.py src/Main.java
```

The module outputs lines like:

```
📁 src/Main.java
----------------
🏛️  class Main [1:42]
    🔧 def Main [3:7]
    🔧 def main [10:22]
```

aligned with the conventions used for the other language modules.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)