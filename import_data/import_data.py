import odoorpc
import openpyxl

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=8069)

# Check available databases
print(odoo.db.list())

# Login
odoo.login('test2', 'krishmanek2003@gmail.com', 'admin')

# Current user
user = odoo.env.user
print(user.name)            # name of the user connected
print(user.company_id.name)
try:
    wb = openpyxl.load_workbook('/home/krish/workspace/18/odoo_tutorials/import_data/Work Centers.xlsx')
    ws = wb.active
    print(ws)
    for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,                
        max_col=None, values_only=True):
        print(f"Record 0 {record[0]}, Record 1 {record[1]}, Record 2 {record[2]}, Record 3 {record[3]} ")
        tags = record[1].split(',')
        tag_ids = []
        for tag in tags:    
            search_tags = odoo.env['mrp.workcenter.tag'].search([('name', '=', tag)])
            if search_tags:
                tag_ids.append(search_tags[0])
            else:
                tag_rec = odoo.env['mrp.workcenter.tag'].create({'name' : tag})
                tag_ids.append(tag_rec)
        if record[3]:
            work_centers = record[3].split(',')
            alt_workcenter = []
            for workcenter in work_centers:
                search_alt = odoo.env['mrp.workcenter'].search([('name', '=', workcenter)])
                if search_alt:
                    alt_workcenter.append(search_alt[0]) 
                else:
                    rec = odoo.env['mrp.workcenter'].create({'name' : workcenter})
                    print(f"Alternative Record Created {rec}")
                    if rec:
                        alt_workcenter.append(rec)
            search = odoo.env['mrp.workcenter'].search([('name', '=', record[0])])
            if not search:
                rec = odoo.env['mrp.workcenter'].create({'name' : record[0],
                                                        'tag_ids': [(6, 0 , tag_ids)],
                                                        'code': record[2],
                                                        'alternative_workcenter_ids': [(6, 0, alt_workcenter)]})
                print(f"Record Created {rec}")
            else:
                work_rec = odoo.env['mrp.workcenter'].browse(search[0])       
                if work_rec:
                    work_rec.write({'tag_ids': [(6, 0 , tag_ids)],
                                'code': record[2],
                                'alternative_workcenter_ids': [(6, 0, alt_workcenter)]})
                    print(f"Record Updated {work_rec}")
        else:
            search = odoo.env['mrp.workcenter'].search([('name', '=', record[0])])
            if not search:
                rec = odoo.env['mrp.workcenter'].create({'name' : record[0],
                                                        'tag_ids': [(6, 0 , tag_ids)],
                                                        'code': record[2]})
                print(f"Record Created {rec}")
            else:
                work_rec = odoo.env['mrp.workcenter'].browse(search[0])       
                if work_rec:
                    work_rec.write({'tag_ids': [(6, 0 , tag_ids)],
                                'code': record[2]})
                    print(f"Record Updated {work_rec}")
except Exception as e:
    print(f"Exception {e}")