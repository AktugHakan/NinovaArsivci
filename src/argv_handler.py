from sys import argv


def get_args(**arg_flags) -> dict:
    """
    get_args(flag_name = parameter_count ...)
    get_args()

    Give each flag (without dash '-' at the beggining) that you want to get from argv
    Equal the flag_name to parameter_count that will be given after the flag
    The args that you didn't specified are ignored
    If an arg does not have enough arguments given, rises Exception

    If no argument is given, then all flags and their parameter from argv is taken

    Returns a dictionary which keys are flag names and values are;
        list of parameters if parameter_count > 0
        else None (you can check whether the flag is given or not with "flag_name in arg_dict")

    Example:
        Assume that your program is started as
        python program.py -a -user username password -count 12

        You should call the function as:
            get_args(a=0, user=2, count=1)
            or
            get_args()
        Which returns
            {"a" = None, "user" = [username, password], "count" = ["12"]}

    """
    arg_dict = dict()
    arg_index = 0
    if arg_flags:
        arg_index += 1
        while arg_index < len(argv):
            flag = argv[arg_index]
            flag = flag[1:]  # remove dash sign before the flag
            if flag in arg_flags:
                if arg_flags[flag] == 0:
                    arg_dict[flag] = None
                else:
                    params = list()
                    for _ in range(arg_flags[flag]):
                        arg_index += 1

                        if argv[arg_index].startswith("-"):
                            raise Exception(
                                f"Not enough parameter(s) given for the flag '-{flag}'"
                            )

                        params.append(argv[arg_index])
                    arg_dict[flag] = tuple(params)

            arg_index += 1
    else:
        flag = None
        params = list()
        while arg_index < len(argv):
            if argv[arg_index].startswith("-"):
                if len(params) > 0:
                    arg_dict[flag] = tuple(params)
                else:
                    arg_dict[flag] = None
                flag = argv[arg_index][1:]
                params = list()
            else:
                params.append(argv[arg_index])
            arg_index += 1

        if len(params) > 0:
            arg_dict[flag] = tuple(params)
        else:
            arg_dict[flag] = None
    return arg_dict
