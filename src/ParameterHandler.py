class ParameterHandler:
    def __init__(self):
        self.activation_threshold = 0.0
        self.max_activation = 0.0
        self.min_activation = 0.0
        self.habituation_threshold = 0.0
        self.sensitization_threshold = 0.0
        self.max_weight = 0.0
        self.min_weight = 0.0

        self.backfall_curvature = 0.0
        self.backfall_steepness = 0.0
        self.max_transmitter_weight = 0.0
        self.min_transmitter_weight = 0.0

        self.short_habituation_curvature = 0.0
        self.short_habituation_steepness = 0.0
        self.short_sensitization_curvature = 0.0
        self.short_sensitization_steepness = 0.0
        self.short_dehabituation_curvature = 0.0
        self.short_dehabituation_steepness = 0.0
        self.short_desensitization_curvature = 0.0
        self.short_desensitization_steepness = 0.0

        self.long_habituation_curvature = 0.0
        self.long_habituation_steepness = 0.0
        self.long_sensitization_curvature = 0.0
        self.long_sensitization_steepness = 0.0
        self.long_dehabituation_curvature = 0.0
        self.long_dehabituation_steepness = 0.0
        self.long_desensitization_curvature = 0.0
        self.long_desensitization_steepness = 0.0

        self.presynaptic_potential_curvature = 0.0
        self.presynaptic_potential_steepness = 0.0
        self.presynaptic_backfall_curvature = 0.0
        self.presynaptic_backfall_steepness = 0.0

        self.long_learning_weight_reduction_curvature = 0.0
        self.long_learning_weight_reduction_steepness = 0.0
        self.long_learning_weight_backfall_curvature = 0.0
        self.long_learning_weight_backfall_steepness = 0.0

