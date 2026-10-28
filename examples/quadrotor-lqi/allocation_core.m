function omega2_raw = allocation_core(tau,mix_inv,collective)
%#codegen
% 前/左/后/右的平方转速；物理限幅和一阶动态留在原生MotorDynamics。
assert(isequal(size(tau),[3 1]) && isequal(size(mix_inv),[4 4]) && isscalar(collective));
assert(all(isfinite(tau)) && all(isfinite(mix_inv(:))) && isfinite(collective) && collective>=0);
omega2_raw = mix_inv*[collective;tau];
end
