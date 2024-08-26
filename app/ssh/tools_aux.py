def cantidad_horas_activo(seconds: int) -> str:
    days = seconds // 86400
    remaining_seconds = seconds % 86400
    hours = remaining_seconds // 3600
    remaining_seconds %= 3600
    minutes = remaining_seconds // 60
    remaining_seconds %= 60
    secs = remaining_seconds
    
    
    if days == 0:
        return f"{hours:02}:{minutes:02}:{secs:02}"
    elif days == 1:
        return f"{days} día {hours:02}:{minutes:02}:{secs:02}"
    else:
        return f"{days} días {hours:02}:{minutes:02}:{secs:02}"