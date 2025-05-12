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
    wb = openpyxl.load_workbook('/home/krish/workspace/18/odoo_tutorials/import_data/Product Categories.xlsx')
    ws = wb.active
    count = len([row for row in ws if not all([cell.value == None for cell in row])])
    # Print the number of non-empty rows
    print(f"no of rows: {count}")
    for record in ws.iter_rows(min_row=2, max_row=count, min_col=None,                
        max_col=None, values_only=True):
        #print(f"Record 0 {record[0]}, Record 1 {record[1]} ")
        search_category = None
        if record[1]:
            category_name = record[0].removeprefix(record[1] + " / ")
            product_category = record[1].split(' / ')
            if product_category[-1] !='All':
                search_category = odoo.env['product.category'].search([('name', '=', product_category[-1])])  
                if not search_category:
                    parent_category = odoo.env['product.category'].search([('name', '=', product_category[0])])
                    search_category_id = odoo.env['product.category'].create({'name' : product_category[-1],
                                                                              'parent_id': parent_category[0]})
                    search_category = search_category_id
            else:      
                search_category = odoo.env['product.category'].search([('name', '=', product_category)])
                if not search_category:
                    search_category_id = odoo.env['product.category'].create({'name' : product_category})
                    search_category = [search_category_id]
        else:
            category_name = record[0]
        search_category_name = odoo.env['product.category'].search([('name', '=', category_name)])
        if not search_category_name:
            i = 0
            if search_category:
                rec = odoo.env['product.category'].create({'name' : category_name,
                                                       'parent_id' : search_category[0]})
            else:
                rec = odoo.env['product.category'].create({'name' : category_name})
            print(f"Record Created {i}, {rec}")
            i+=1
            
except Exception as e:
    print(f"Exception {e}")