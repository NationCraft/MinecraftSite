from datetime import datetime, timedelta, tzinfo


def local_to_utc(date_input):
    tzoffset = date_input.tzinfo.utcoffset()
    date = (date_input - tzoffset).replace(tzinfo=UTC())
    return date


def utc_to_local(date_input, timezone_output):
    if timezone_output == 'PST':
        tz_output = PST
    elif timezone_output == 'PDT':
        tz_output = PDT
    elif timezone_output == 'CST':
        tz_output = CST
    elif timezone_output == 'CDT':
        tz_output = CDT
    elif timezone_output == 'EST':
        tz_output = EST
    elif timezone_output == 'EDT':
        tz_output = EDT
    try:
        tzoffset = tz_output.utcoffset(tz_output)
        date = (date_input + tzoffset)
        return date
    except Exception as e:
        print(e)


class UTC(tzinfo):
    def utcoffset(self, *dt):
        return timedelta(hours=0)

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        pass


class PST(tzinfo):
    def utcoffset(self, *dt):
        return timedelta(hours=-8)

    def tzname(self, dt):
        return 'PacificStandard'

    def dst(self, dt):
        pass


class PDT(tzinfo):
    def utcoffset(self, *dt):
        return timedelta(hours=-7)

    def tzname(self, dt):
        return 'PacificDaylight'

    def dst(self, dt):
        pass


class CST(tzinfo):
    def utcoffset(self, *dt):
        return timedelta(hours=-6)

    def tzname(self, dt):
        return 'CentralStandard'

    def dst(self, dt):
        pass


class CDT(tzinfo):
    def utcoffset(self, *dt):
        return timedelta(hours=-5)

    def tzname(self, dt):
        return 'CentralDaylight'

    def dst(self, dt):
        pass


class EST(tzinfo):
    def utcoffset(self, *dt):
        return timedelta(hours=-5)

    def tzname(self, dt):
        return 'EasternStandard'

    def dst(self, dt):
        pass


class EDT(tzinfo):
    def utcoffset(self, *dt):
        return timedelta(hours=-4)

    def tzname(self, dt):
        return 'EasternDaylight'

    def dst(self, dt):
        pass
