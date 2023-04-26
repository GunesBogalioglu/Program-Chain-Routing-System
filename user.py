# Kullanıcılara güvenme sayı yerine karakter veya karakter yerine sayı girebilirler.
def get_loss_settings():
    """Kullanıcıdan kayıplı/kayıpsız ayarını ister.

    Returns:
        bool: True - Lossless, False - Lossy
    """
    ans = input("Lossy or Lossless (lossy,lossless)")
    return bool(str(ans).lower() in ("lossless", "1", "not lossy"))


def get_quality_settings():
    ans = input("İstenilen kalite (sayı) ayarı:")
    return int(ans)
