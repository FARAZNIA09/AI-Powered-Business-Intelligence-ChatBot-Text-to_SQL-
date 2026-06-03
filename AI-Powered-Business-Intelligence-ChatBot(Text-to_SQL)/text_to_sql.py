from utils import extract_top_n, SYNONYMS, match_keywords

def convert_to_sql(user_query):
    query = user_query.lower()

    # RULE 1A: Top Products by PROFIT
    if (
        match_keywords(query, SYNONYMS["top"]) and
        match_keywords(query, SYNONYMS["product"]) and
        match_keywords(query, SYNONYMS["profit"])
    ):
        top_n = extract_top_n(query)
        return f"""
        SELECT TOP {top_n} p.product_name, SUM(s.profit) AS total_profit
        FROM Sales s
        JOIN Products p ON s.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_profit DESC;
        """

    # RULE 1B: Top Products by SALES / REVENUE (Fixes your screenshot issue!)
    elif (
        match_keywords(query, SYNONYMS["top"]) and
        match_keywords(query, SYNONYMS["product"]) and
        match_keywords(query, SYNONYMS["sales"])
    ):
        top_n = extract_top_n(query)
        return f"""
        SELECT TOP {top_n} p.product_name, SUM(s.revenue) AS total_revenue
        FROM Sales s
        JOIN Products p ON s.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_revenue DESC;
        """

    # RULE 2: Regional Sales performance
    elif (
        match_keywords(query, SYNONYMS["sales"]) and
        match_keywords(query, SYNONYMS["region"])
    ):
        return """
        SELECT c.region, SUM(s.revenue) AS total_revenue
        FROM Sales s
        JOIN Customers c ON s.customer_id = c.customer_id
        GROUP BY c.region;
        """

    # RULE 3: Time-based trendlines
    elif "month" in query or "trend" in query:
        return """
        SELECT MONTH(s.sale_date) AS month, SUM(s.revenue) AS total_revenue
        FROM Sales s
        GROUP BY MONTH(s.sale_date)
        ORDER BY month;
        """

    return None