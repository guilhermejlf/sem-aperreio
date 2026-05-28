from django.core.paginator import Paginator


def paginate_queryset(queryset, request, page_size=20, max_page_size=100):
    """
    Pagina uma queryset ou lista Python.
    Retorna (paginated_data, pagination_metadata).
    """
    # Parâmetros da requisição
    page_param = request.query_params.get('page', '1')
    page_size_param = request.query_params.get('page_size', str(page_size))

    try:
        page_size_val = int(page_size_param)
    except (ValueError, TypeError):
        page_size_val = page_size

    # Limita page_size ao máximo permitido
    page_size_val = min(page_size_val, max_page_size)
    page_size_val = max(page_size_val, 1)

    try:
        page_num = int(page_param)
    except (ValueError, TypeError):
        page_num = 1

    page_num = max(page_num, 1)

    # Usa Django Paginator
    paginator = Paginator(queryset, page_size_val)

    try:
        page_obj = paginator.page(page_num)
    except Exception:
        # Se a página não existe, retorna a última válida
        if page_num > paginator.num_pages:
            page_obj = paginator.page(paginator.num_pages)
        else:
            page_obj = paginator.page(1)

    # Build URLs para next/previous
    def build_url(target_page):
        params = request.query_params.copy()
        params['page'] = target_page
        params['page_size'] = page_size_val
        return f"{request.path}?{params.urlencode()}"

    metadata = {
        'count': paginator.count,
        'page': page_obj.number,
        'pages': paginator.num_pages,
        'page_size': page_size_val,
        'next': build_url(page_obj.next_page_number()) if page_obj.has_next() else None,
        'previous': build_url(page_obj.previous_page_number()) if page_obj.has_previous() else None,
    }

    return list(page_obj.object_list), metadata
