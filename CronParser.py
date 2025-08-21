import sys

class CronParser:
    """
    A utility class to parse cron expressions into lists of possible values.
    """

    @staticmethod
    def parse_cron_field(expression, min_value, max_value):
        """
        Parse a single cron field expression and return the matching values.

        Args:
            expression (str): A cron expression for a single field, e.g., `"*/5"`, `"1,15,30"`, `"10-20/2"`.
            min_value (int): The minimum valid integer for the field (e.g., 0 for minutes).
            max_value (int): The maximum valid integer for the field (e.g., 59 for minutes).

        Returns:
            list[int]: A sorted list of valid integer values that match the cron expression.
                       If no valid values exist, an empty list is returned.
        """
        values = set()

        if expression == "*":
            return list(range(min_value, max_value+1))

        for part in expression.split(","):

            try:
                if "/" in part:
                    range_part, step_part = part.split("/")
                    step = int(step_part)
                    if step <= 0:
                        raise ValueError(f"Invalid step {step} in expression {expression}")

                    if range_part == "*":
                        start, end = min_value, max_value
                    elif "-" in range_part:
                        start, end = map(int, range_part.split("-"))
                        start = max(min_value,start)
                        end = min(max_value, end)
                    else:
                        start, end = int(range_part), max_value

                    if start > end:
                        raise ValueError(f"Invalid range {start}-{end} in {expression}")

                    values.update(range(start, end+1 , step))

                elif "-" in part:
                    start, end = map(int, part.split("-"))
                    start = max(min_value,start)
                    end = min(max_value, end)

                    if start > end:
                        raise ValueError(f"Invalid range {start}-{end} in {expression}")

                    values.update(range(start, end+1))

                else:
                    if part.isdigit():
                        if int(part)>=min_value and int(part)<=max_value:
                            values.add(int(part))
                    else:
                        raise ValueError(f"Invalid token {part} in {expression}")
            except Exception as e:
                raise ValueError(f"Error parsing part '{part}' in {expression}: {e}")

        return sorted(values)

    @staticmethod
    def format_output(expanded_cron_values):
        for key,value in expanded_cron_values.items():
            if key!="command":
                print(key.ljust(14),' '.join(map(str,value)))
            else:
                print(key.ljust(14),' '.join(value))

    @staticmethod
    def parse_expression(cron_expression):
        fields = cron_expression.split(" ")
        if len(fields)<6:
            print("Cron expression is incorrect! Number of fields in cron expression passed is",len(fields))
        else:
            return {
                "minute" : CronParser.parse_cron_field(fields[0], 0, 59),
                "hour" :  CronParser.parse_cron_field(fields[1], 0, 23),
                "day_of_month" : CronParser.parse_cron_field(fields[2], 1, 31),
                "month" : CronParser.parse_cron_field(fields[3], 1, 12),
                "day of week" : CronParser.parse_cron_field(fields[4], 0, 7),
                "command" : fields[5:]
            }

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Incorrect number of arguments passed")
    else:
        cron_expression = sys.argv[1]
        expanded_cron_values = CronParser.parse_expression(cron_expression)
        CronParser.format_output(expanded_cron_values)
