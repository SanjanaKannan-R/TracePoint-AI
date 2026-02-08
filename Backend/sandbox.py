import subprocess
import tempfile
import os

def run_code(code, lang, timeout=5):
    """
    Execute code in a sandboxed environment
    
    Args:
        code: Source code to execute
        lang: Programming language ('py', 'js', 'java', 'cpp', 'c', etc.)
        timeout: Maximum execution time in seconds
    
    Returns:
        str: Program output or error message
    """
    
    # Map of supported executable languages
    executable_langs = {
        "py": {"ext": ".py", "cmd": ["python3"]},
        "js": {"ext": ".js", "cmd": ["node"]},
    }
    
    if lang not in executable_langs:
        return f"Code execution not supported for {lang}. Only analysis is available."
    
    # Security check - block dangerous imports/requires
    dangerous_patterns = {
        "py": ["os.system", "subprocess", "eval(", "exec(", "__import__", "open("],
        "js": ["require('child_process')", "require('fs')", "eval(", "Function("]
    }
    
    code_lower = code.lower()
    for pattern in dangerous_patterns.get(lang, []):
        if pattern.lower() in code_lower:
            return f"🚫 Security Error: Potentially dangerous operation detected: {pattern}\n\nFor security reasons, operations like file I/O, system commands, and dynamic code execution are not allowed in the sandbox."
    
    # Create temporary file
    lang_config = executable_langs[lang]
    suffix = lang_config["ext"]
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=suffix) as f:
            f.write(code)
            temp_path = f.name
        
        # Build command
        cmd = lang_config["cmd"] + [temp_path]
        
        # Execute with timeout
        try:
            result = subprocess.run(
                cmd,
                timeout=timeout,
                capture_output=True,
                text=True,
                cwd=tempfile.gettempdir()
            )
            
            # Return output or error
            if result.returncode == 0:
                output = result.stdout.strip()
                return output if output else "✅ Program executed successfully (no output)"
            else:
                error = result.stderr.strip()
                return f"❌ Execution Error:\n{error}" if error else f"Exit code: {result.returncode}"
        
        except subprocess.TimeoutExpired:
            return f"⏱️ Timeout Error: Execution exceeded {timeout} seconds.\n\nYour code may have an infinite loop or is taking too long to execute."
        
        except FileNotFoundError:
            interpreter_names = {"py": "Python 3", "js": "Node.js"}
            interpreter = interpreter_names.get(lang, lang)
            return f"❌ Error: {interpreter} interpreter not found on server.\n\nPlease contact the administrator."
        
        except Exception as e:
            return f"❌ Execution Error: {str(e)}"
    
    finally:
        # Clean up temporary file
        try:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        except:
            pass


def validate_code_syntax(code, lang):
    """
    Validate code syntax without executing
    
    Args:
        code: Source code to validate
        lang: Programming language
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if lang == "py":
        try:
            compile(code, '<string>', 'exec')
            return True, None
        except SyntaxError as e:
            return False, f"Syntax Error at line {e.lineno}: {e.msg}"
    
    elif lang == "js":
        # Basic JavaScript validation
        if code.count('{') != code.count('}'):
            return False, "Syntax Error: Mismatched braces"
        if code.count('(') != code.count(')'):
            return False, "Syntax Error: Mismatched parentheses"
        if code.count('[') != code.count(']'):
            return False, "Syntax Error: Mismatched brackets"
        return True, None
    
    # For other languages, skip syntax validation (would need language-specific parsers)
    return True, None


def get_language_info(lang):
    """
    Get information about a programming language
    
    Args:
        lang: Language code
    
    Returns:
        dict: Language information
    """
    languages = {
        "py": {
            "name": "Python",
            "version": "3.x",
            "executable": True,
            "description": "High-level, interpreted programming language"
        },
        "js": {
            "name": "JavaScript",
            "version": "ES6+",
            "executable": True,
            "description": "Dynamic scripting language for web"
        },
        "java": {
            "name": "Java",
            "executable": False,
            "description": "Object-oriented compiled language"
        },
        "cpp": {
            "name": "C++",
            "executable": False,
            "description": "High-performance compiled language"
        },
        "c": {
            "name": "C",
            "executable": False,
            "description": "Low-level compiled language"
        },
        "html": {
            "name": "HTML",
            "executable": False,
            "description": "Markup language for web pages"
        },
        "css": {
            "name": "CSS",
            "executable": False,
            "description": "Styling language for web pages"
        },
        "sql": {
            "name": "SQL",
            "executable": False,
            "description": "Database query language"
        }
    }
    
    return languages.get(lang, {
        "name": lang.upper(),
        "executable": False,
        "description": "Programming language"
    })