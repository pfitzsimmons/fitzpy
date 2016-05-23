'''


A wrapper around optparse.OptionParser that makes defining options for a script even easier.


-------------------------myscript.py--------------------

def main():
    options = Options.from_argv()
    if options.action == 'audit':
        some_function(options.account_id, dry_run=options.dry_run)
    elif ...
    else:
        options.print_help()
    


class Options(ScriptOptions)
    account_id = Opt(required=True, help="The account you want to audit")
    dry_run = Opt(default=False, action='store_true', help="Set this option to print what would happen without execution")
    action = Opt(default='audit', choices=['audit', 'detect_fraud', 'validate_books'], help="The action you want to perform")

if __name__ == '__main__':
    main()

---------------------
Now you can run your script and include the options:

python myscript.py --acount-id=7
python myscript.py -a 7 --dry-run





'''

from optparse import OptionParser
import sys

from .propertized import Propertized, Prop

class Opt(Prop):
    def __init__(self, default=None, required=False, help='', choices=(), action=None, type=None, **kwargs):
        super(Opt, self).__init__(default=default, help=help, choices=choices, **kwargs)
        self.default = default
        self.help = help
        self.choices = choices
        self.extra = kwargs
        self.action = action
        self.required = required
        self.type = type



class ScriptOptions(Propertized):
    def __init__(self, **kwargs):
        parser = None
        self._hydrate_from_kwargs(**kwargs)

    @classmethod
    def from_argv(cls, argv=None, **defaults):
        if not argv:
            argv = sys.argv
        parser = cls._build_option_parser(**defaults)        
        parsed_options = parser.parse_args(argv)[0]
        script_options = cls()
        script_options._hydrate_script_options_from_parsed_options(parsed_options, parser)
        return script_options

    @classmethod
    def _build_option_parser(cls, **defaults):
        reserved_letters = set(['h'])
        parser = OptionParser()
        for opt in cls.list_class_props():
            args = []
            kwargs = {}
            letter = opt.attr_name[0]
            if letter not in reserved_letters:
                args.append('-' + letter)
                reserved_letters.add(letter)
            args.append('--' + opt.attr_name.replace('_', '-'))
            if opt.default is not None:
                kwargs['default'] = opt.default
            if opt.attr_name in defaults:
                kwargs['default'] = defaults[opt.attr_name]
            kwargs['help'] = ''
            if opt.help:
                kwargs['help'] = opt.help
            if opt.choices:
                if kwargs['help']:
                    kwargs['help'] += '. '
                kwargs['help'] += 'Choices are: ' + ", ".join(opt.choices)
            if opt.required:
                kwargs['help'] = '(Required) ' + kwargs['help']
            if opt.action:
                kwargs['action'] = opt.action
            if opt.choices:
                kwargs['choices'] = opt.choices
            kwargs.update(opt.extra)
            parser.add_option(*args, **kwargs)
        return parser

    def _hydrate_script_options_from_parsed_options(self, parsed_options, parser):
        self.parser = parser
        for opt in self.list_class_props():
            if opt.required and getattr(parsed_options, opt.attr_name) == None:
                sys.stderr.write("\n\nError! The option %s is required\n\n" % opt.attr_name)
                parser.print_help()
                sys.exit(1)
            val = getattr(parsed_options, opt.attr_name)
            opt_type = opt.type
            if not opt_type and opt.default != None:
                opt_type = opt.default.__class__
            if opt_type:
                if opt_type == bool:
                    val = str(val).lower() == 'true' or val == 1
                try:
                    val = opt_type(val)
                except Exception:
                    pass
            setattr(self, opt.attr_name, val)
        
        
    def print_help(self):
        self.parser.print_help()
    
