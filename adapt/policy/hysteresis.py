class HysteresisController:
    """
    Prevents resource allocation thrashing and continuous oscillatory actuation.
    Enforces minimum cooldown ticks and minimum quota change dead-band.
    """
    def __init__(self, cooldown_ticks: int = 3, minimum_change: float = 8.0):
        self.cooldown_ticks = cooldown_ticks
        self.minimum_change = minimum_change
        self.ticks_since_last_change: int = 999
        self.last_allocated_quota: float = 50.0

    def should_apply_change(self, target_quota: float, current_quota: float, is_critical: bool = False) -> bool:
        """
        Determines whether allocation modification should proceed.
        Critical emergencies can override cooldown.
        """
        self.ticks_since_last_change += 1
        
        # Critical bypass
        if is_critical and abs(target_quota - current_quota) > 5.0:
            self.ticks_since_last_change = 0
            self.last_allocated_quota = target_quota
            return True
            
        # Check cooldown
        if self.ticks_since_last_change < self.cooldown_ticks:
            return False
            
        # Check minimum change dead-band
        if abs(target_quota - current_quota) < self.minimum_change:
            return False
            
        self.ticks_since_last_change = 0
        self.last_allocated_quota = target_quota
        return True

    def reset(self, initial_quota: float = 50.0):
        self.ticks_since_last_change = 999
        self.last_allocated_quota = initial_quota
