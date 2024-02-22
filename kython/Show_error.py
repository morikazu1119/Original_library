from kython.Slack_send import slack_msg

def custom_exc(shell, etype, evalue, tb, tb_offset=None):
    from IPython.core.ultratb import AutoFormattedTB
    itb = AutoFormattedTB(mode='Plain', tb_offset=1)
    shell.showtraceback((etype, evalue, tb), tb_offset=tb_offset)
    stb = itb.structured_traceback(etype, evalue, tb)
    sstb = itb.stb2text(stb)

    # ここに例外発生時に実行するコードを書く
    slack_msg("ERROR: 例外が発生しました。")

    return sstb

def show_err():
    from IPython import get_ipython
    get_ipython().set_custom_exc((Exception,), custom_exc)



