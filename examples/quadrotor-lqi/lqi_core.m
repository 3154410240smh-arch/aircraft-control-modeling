function tau = lqi_core(eta,rate,xi,K)
%#codegen
% 纯代数控制律；xi为外部原生Integrator的状态，无persistent。
assert(isequal(size(eta),[3 1]) && isequal(size(rate),[3 1]));
assert(isequal(size(xi),[3 1]) && isequal(size(K),[3 9]));
assert(all(isfinite(eta)) && all(isfinite(rate)) && all(isfinite(xi)) && all(isfinite(K(:))));
tau = -K*[eta;rate;xi];
end
