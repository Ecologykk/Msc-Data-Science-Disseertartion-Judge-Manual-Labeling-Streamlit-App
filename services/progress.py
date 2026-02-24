from __future__ import annotations


def is_response_complete(response: dict[str, str]) -> bool:
    decisao = str(response.get("decisao", "")).strip()
    confianca = str(response.get("confianca", "")).strip()
    justificacao = str(response.get("justificacao", "")).strip()

    if not (decisao and confianca):
        return False
    if confianca == "Não Confiante" and not justificacao:
        return False
    return True


def compute_progress(
    case_ids: list[str],
    responses: dict[str, dict[str, str]],
) -> tuple[int, int, float]:
    total = len(case_ids)
    if total == 0:
        return 0, 0, 0.0

    answered = 0
    for case_id in case_ids:
        response = responses.get(case_id, {})
        if is_response_complete(response):
            answered += 1

    progress = answered / total
    return answered, total, progress


def first_incomplete_index(
    ordered_case_ids: list[str],
    responses: dict[str, dict[str, str]],
) -> int:
    for index, case_id in enumerate(ordered_case_ids):
        response = responses.get(case_id, {})
        if not is_response_complete(response):
            return index
    return 0
