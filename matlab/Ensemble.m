classdef Ensemble < handle
    
    properties
        N;
        D;
        va;
        vfield;
        ens;
    end
    
    methods
        %constructor function for an ensemble
        function obj = Ensemble(N,D,va,vfield)
            obj.N = N;
            obj.D = D;
            obj.va = va;
            obj.vfield = vfield;
            obj.ens = cell(N);
            for i = 1:N
                obj.ens{i,1}=Swimmer(D, va, vfield);
            end
        end
        %time evolution for every swimmer in the ensemble
        function timeE(obj, T_total)
            for i = 1:obj.N
                obj.ens{i,1}.timeE(T_total);
            end
        end
        %Mean Squared Displacement calculated from the ensemble
        function msd = MSD(obj, time)
            t=zeros(1,obj.N);
            for i=1:obj.N
                t(i) = obj.ens{i}.traj(time, 1)^2+obj.ens{i}.traj(time,2)^2;
            end
            
            msd = mean(t);
        end
        
        %sedimentation profile
        function profile = sedP(obj, steadyT, persistant)
            z = [];
            for i = 1:obj.N
                z=[z, obj.ens{i}.traj(steadyT:persistant:end, 2)];
            end
            
            profile = histogram(z,30);
        end
        
        function orientation = oriP(obj, steadyT, persistant)
            o = [];
            for i = 1:obj.N
                for tt = steadyT:persistant:length(obj.ens{i}.ori)
                    if obj.ens{i}.traj(tt, 2)>-48
                        o = [o, obj.ens{i}.ori(tt)];
                    end
                end
            end
            o = wrapToPi(o);
            orientation = histogram(o);
        end

    end
    
end
