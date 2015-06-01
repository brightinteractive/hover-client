#!/usr/bin/python
# -*- coding: utf-8 -*-


from hover.client import HoverClient


def main():

    module = AnsibleModule(
        argument_spec=dict(
            domain=dict(required=True, default=None),
            username=dict(required=True, default=None),
            password=dict(required=True, default=None),
            state=dict(choices=['present', 'absent'], default='present'),
            type=dict(choices=['A',
                               'ALIAS',
                               'CNAME',
                               'MX',
                               'SPF',
                               'URL',
                               'TXT',
                               'NS',
                               'SRV',
                               'NAPTR',
                               'PTR',
                               'AAAA',
                               'SSHFP',
                               'HINFO',
                               'POOL'], default='A'),
            name=dict(required=True, default=None),
            value=dict(required=True, default=None),
        ),
        add_file_common_args=True,
        supports_check_mode=False
    )

    params = module.params
    changed = False

    hc = HoverClient(username=params['username'],
                     password=params['password'],
                     domain_name=params['domain'])

    record = hc.get_record(name=params['name'], type=params['type'])

    if params['state'] == 'present':

        if record is None:
            hc.add_record(name=params['name'],
                          type=params['type'],
                          content=params['value'])
            changed = True
        else:

            if record['content'] != params['value']:
                hc.update_record(name=params['name'],
                                 type=params['type'],
                                 content=params['value'])
                changed = True
    else:
        if record is not None:
            hc.remove_record(name=params['name'],
                             type=params['type'])
            changed = True

    module.exit_json(changed=changed)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()