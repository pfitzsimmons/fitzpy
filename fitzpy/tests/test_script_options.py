
from nose.tools import ok_, eq_
from fitzpy.script_options import ScriptOptions, Opt


class Options(ScriptOptions):
    account_id = Opt(required=True, help="The account you want to audit", type=int)
    dry_run = Opt(default=False, action='store_true', help="Set this option to print what would happen without execution")
    action = Opt(default='audit', choices=['audit', 'detect_fraud', 'validate_books'], help="The action you want to perform")

def test_basic():
    args = ['--account-id=100', '--action=validate_books']

    options = Options.from_argv(args)
    eq_(100, options.account_id)
    eq_('validate_books', options.action)
    
    args = ['--account-id=100']
    options = Options.from_argv(args)
    eq_('audit', options.action)


    

