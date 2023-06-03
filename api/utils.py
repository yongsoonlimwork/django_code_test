def process_packs_data(pack1_data, pack2_data, customer_id):
    pack1 = None
    pack2 = None

    for customer_data in pack1_data:
        if customer_data['customer_id'] == customer_id:
            pack1 = format_pack_data(customer_data['pack_data'])
            break

    for customer_data in pack2_data:
        if customer_data['customer_id'] == customer_id:
            pack2 = format_pack_data(customer_data['pack_data'])
            break

    return [pack1, pack2]


def format_pack_data(pack_data):
    info = []
    for data in pack_data:
        info.append(f'{data["ingredient"]} {data["quantity"]}{data["unit"]}')
    return info
