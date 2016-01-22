# -*- coding: utf-8 -*-
#
# This file is part of DoJSON
# Copyright (C) 2015 CERN.
#
# DoJSON is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Test suite for DoJSON."""

from click.testing import CliRunner

import json


def test_cli_do_marc21_from_xml():
    """Test MARC21 loading from XML."""
    from dojson import cli
    from test_core import RECORD_SIMPLE, RECORD_999_FIELD

    expected = [{
        'main_entry_personal_name': {'personal_name': 'Donges, Jonathan F'}
    }]
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open('record.xml', 'wb') as f:
            f.write(RECORD_SIMPLE.encode('utf-8'))

        with open('record_999.xml', 'wb') as f:
            f.write(RECORD_999_FIELD.encode('utf-8'))

        result = runner.invoke(
            cli.missing_fields,
            ['-i', 'record.xml', '-l', 'marcxml', 'marc21']
        )
        assert result.output == ''
        assert result.exit_code == 0

        result = runner.invoke(
            cli.missing_fields,
            ['-i', 'record_999.xml', '-l', 'marcxml', 'marc21']
        )
        assert result.output == '999__\n'
        assert result.exit_code == 1

        result = runner.invoke(
            cli.apply_rule,
            ['-i', 'record.xml', '-l', 'marcxml', 'marc21']
        )
        data = json.loads(result.output)
        assert expected == data

        result = runner.invoke(
            cli.apply_rule,
            ['-i', 'record_999.xml', '-l', 'marcxml', 'marc21']
        )
        data = json.loads(result.output)
        assert {} == data[0]
        assert result.exit_code == 0

        result = runner.invoke(
            cli.apply_rule,
            ['-i', 'record.xml', '-l', 'marcxml', '--strict', 'marc21']
        )
        assert result.exit_code == -1


def test_cli_do_marc21_from_json():
    """Test MARC21 loading from XML."""
    from dojson import cli
    from dojson.contrib.marc21.utils import create_record
    from test_core import RECORD_SIMPLE

    expected = {
        'main_entry_personal_name': {'personal_name': 'Donges, Jonathan F'}
    }
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open('record.json', 'wb') as fp:
            record = create_record(RECORD_SIMPLE)
            fp.write(json.dumps(record).encode('utf-8'))

        result = runner.invoke(
            cli.missing_fields,
            ['-i', 'record.json', 'marc21']
        )
        assert '' == result.output
        assert 0 == result.exit_code

        result = runner.invoke(
            cli.apply_rule,
            ['-i', 'record.json', 'marc21']
        )
        data = json.loads(result.output)
        assert expected == data

        # FIXME
        result = runner.invoke(
            cli.apply_rule,
            ['-i', 'record.json', '-d', 'marcxml', 'marc21']
        )
        data = result  # json.loads(result.output)
        assert expected == data


#  def test_cli_do_marcxml_from_json_with_xslt():
#      """Test MARC21 loading from XML."""
#      from dojson import cli
#      from dojson.contrib.marc21.utils import create_record
#      from test_core import RECORD_SIMPLE
#      from test_contrib_to_marc21_utils import RECORD_XSLT, RECORD_EXPECTED

#      runner = CliRunner()

#      with runner.isolated_filesystem():
#          with open('record.json', 'wb') as fp:
#              record = create_record(RECORD_SIMPLE)
#              fp.write(json.dumps(record).encode('utf-8'))
#          with open('record.xsl', 'wb') as f:
#              f.write(RECORD_XSLT.encode('utf-8'))

#          result = runner.invoke(
#              cli.apply_rule_marcxml,
#              ['-i', 'record.json',
#               '-f', 'record.xsl']
#          )
#          assert "{}\n".format(RECORD_EXPECTED) == result.output


def test_cli_do_marcxml_from_xml_with_xslt():
    """Test MARC21 loading from XML."""
    from dojson import cli
    from test_core import RECORD_SIMPLE
    from test_contrib_to_marc21_utils import RECORD_XSLT, RECORD_EXPECTED

    #  import pudb; pudb.set_trace()  # XXX BREAKPOINT
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open('record.xml', 'wb') as f:
            f.write(RECORD_SIMPLE.encode('utf-8'))
        with open('record.xsl', 'wb') as f:
            f.write(RECORD_XSLT.encode('utf-8'))

        result = runner.invoke(
            cli.apply_rule_marcxml,
            ['-i', 'record.xml', '-l', 'marcxml',
             '-f', 'record.xsl']
        )
        assert "{}\n".format(RECORD_EXPECTED) == result.output
