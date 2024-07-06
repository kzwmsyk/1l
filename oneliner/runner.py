from oneliner.scanner import Scanner
from oneliner.error import ScanError, ErrorReporter
from oneliner.parser import Parser
from oneliner.ast_printer import AstPrinter
from oneliner.interpreter import Interpreter
from oneliner.resolver import Resolver
import readline
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Runner:

    def __init__(self, args):
        self.is_debug = args.debug
        self.error_reporter = ErrorReporter()
        self.interpreter = Interpreter(self.error_reporter)

    def run_file(self, script_path: str, args: list[str] = []):
        with open(script_path, 'r', encoding='utf-8') as file:
            code = file.read()
            self.run(code, args)
            if self.error_reporter.has_error:
                exit(65)
            if self.error_reporter.has_runtime_error:
                exit(70)

    def run_prompt(self):
        readline.parse_and_bind("tab: complete")

        while True:
            try:
                # 入力を読み込む
                code = input(">")
                # 入力を評価して結果を表示
                self.run(code)
                self.error_reporter.reset()
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
            except EOFError:
                print("\nexit")
                break
            except Exception as e:
                logger.exception("error: %s", e)

    def run(self, code: str, args: list[str] = []):
        scanner = Scanner(code, self.error_reporter)
        try:
            tokens = scanner.scan_tokens()

            parser = Parser(tokens, self.error_reporter)
            statements = parser.parse()

            # 構文エラーがあれば停止
            if (self.error_reporter.has_error):
                return

            if self.is_debug:
                printer = AstPrinter(self)
                print(printer.print(statements))

            resolver = Resolver(self.interpreter, self.error_reporter)
            resolver.resolve(statements)
            if self.error_reporter.has_error:
                return

            self.interpreter.interpret(statements)

        except ScanError as e:
            self.report(e.line, e.current, e.message)
            return
