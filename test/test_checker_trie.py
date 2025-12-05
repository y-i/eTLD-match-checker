from typing import Callable, Optional

import pytest
from src.checker_trie import ETLDChecker


@pytest.fixture(scope='module', autouse=True)
def checkPublicSuffix() -> Callable[[str], Optional[str]]:
    checker = ETLDChecker()
    checker.initialize_from_file('test/list.dat')

    def checkPublicSuffixImpl(domain: str) -> Optional[str]:
        result = checker.check(domain)
        print(result)
        return result.data.root_domain if result.is_valid else None

    return checkPublicSuffixImpl


class TestNone:
    data = [
        (None, None),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


class TestMixed:
    data = [
        ('COM', None),
        ('example.COM', 'example.com'),
        ('WwW.example.COM', 'example.com'),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


class TestLeadingDot:
    data = [
        ('.com', None),
        ('.example', None),
        ('.example.com', None),
        ('.example.example', None),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


@pytest.mark.skip(reason='NOT Implemented')
class TestUnlistedTLD:
    data = [
        ('example', None),
        ('example.example', 'example.example'),
        ('b.example.example', 'example.example'),
        ('a.b.example.example', 'example.example'),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


@pytest.mark.skip(reason='Commented out')
class TestListedButNotInternetTLD:
    data = [
        ('local', None),
        ('example.local', None),
        ('b.example.local', None),
        ('a.b.example.local', None),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


class TestOnly1Rules:
    data = [
        ('biz', None),
        ('domain.biz', 'domain.biz'),
        ('b.domain.biz', 'domain.biz'),
        ('a.b.domain.biz', 'domain.biz'),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


class TestSome2LevelRules:
    data = [
        ('com', None),
        ('example.com', 'example.com'),
        ('b.example.com', 'example.com'),
        ('a.b.example.com', 'example.com'),
        ('uk.com', None),
        ('example.uk.com', 'example.uk.com'),
        ('b.example.uk.com', 'example.uk.com'),
        ('a.b.example.uk.com', 'example.uk.com'),
        ('test.ac', 'test.ac'),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


class TestOnly1WildcardRules:
    data = [
        ('mm', None),
        ('c.mm', None),
        ('b.c.mm', 'b.c.mm'),
        ('a.b.c.mm', 'b.c.mm'),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


class TestMoreComplexTLD:
    data = [
        ('jp', None),
        ('test.jp', 'test.jp'),
        ('www.test.jp', 'test.jp'),
        ('ac.jp', None),
        ('test.ac.jp', 'test.ac.jp'),
        ('www.test.ac.jp', 'test.ac.jp'),
        ('kyoto.jp', None),
        ('test.kyoto.jp', 'test.kyoto.jp'),
        ('ide.kyoto.jp', None),
        ('b.ide.kyoto.jp', 'b.ide.kyoto.jp'),
        ('a.b.ide.kyoto.jp', 'b.ide.kyoto.jp'),
        ('c.kobe.jp', None),
        ('b.c.kobe.jp', 'b.c.kobe.jp'),
        ('a.b.c.kobe.jp', 'b.c.kobe.jp'),
        ('city.kobe.jp', 'city.kobe.jp'),
        ('www.city.kobe.jp', 'city.kobe.jp'),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


class TestAWildcardRuleAndExceptions:
    data = [
        ('ck', None),
        ('test.ck', None),
        ('b.test.ck', 'b.test.ck'),
        ('a.b.test.ck', 'b.test.ck'),
        ('www.ck', 'www.ck'),
        ('www.www.ck', 'www.ck'),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


class TestUSK12:
    data = [
        ('us', None),
        ('test.us', 'test.us'),
        ('www.test.us', 'test.us'),
        ('ak.us', None),
        ('test.ak.us', 'test.ak.us'),
        ('www.test.ak.us', 'test.ak.us'),
        ('k12.ak.us', None),
        ('test.k12.ak.us', 'test.k12.ak.us'),
        ('www.test.k12.ak.us', 'test.k12.ak.us'),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


class TestIDNLabels:
    data = [
        ('食狮.com.cn', '食狮.com.cn'),
        ('食狮.公司.cn', '食狮.公司.cn'),
        ('www.食狮.公司.cn', '食狮.公司.cn'),
        ('shishi.公司.cn', 'shishi.公司.cn'),
        ('公司.cn', None),
        ('食狮.中国', '食狮.中国'),
        ('www.食狮.中国', '食狮.中国'),
        ('shishi.中国', 'shishi.中国'),
        ('中国', None),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld


@pytest.mark.skip(reason='NOT Implemented')
class TestSameAsAboveButPunycoded:
    data = [
        ('xn--85x722f.com.cn', 'xn--85x722f.com.cn'),
        ('xn--85x722f.xn--55qx5d.cn', 'xn--85x722f.xn--55qx5d.cn'),
        ('www.xn--85x722f.xn--55qx5d.cn', 'xn--85x722f.xn--55qx5d.cn'),
        ('shishi.xn--55qx5d.cn', 'shishi.xn--55qx5d.cn'),
        ('xn--55qx5d.cn', None),
        ('xn--85x722f.xn--fiqs8s', 'xn--85x722f.xn--fiqs8s'),
        ('www.xn--85x722f.xn--fiqs8s', 'xn--85x722f.xn--fiqs8s'),
        ('shishi.xn--fiqs8s', 'shishi.xn--fiqs8s'),
        ('xn--fiqs8s', None),
    ]

    @pytest.mark.parametrize('domain, etld', data)
    def test(
        self, domain: str, etld: str, checkPublicSuffix: Callable[[str], Optional[str]]
    ) -> None:
        assert checkPublicSuffix(domain) == etld
