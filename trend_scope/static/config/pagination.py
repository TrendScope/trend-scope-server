def get_pagination_result(paginator, total_items):
    items_per_page = paginator.page_size
    current_page = paginator.page.number
    return {
        'items_per_page': items_per_page,
        'current_page': current_page,
        'total_items': total_items
}